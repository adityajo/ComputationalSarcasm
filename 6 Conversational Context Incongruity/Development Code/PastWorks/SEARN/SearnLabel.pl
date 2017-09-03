#!/usr/bin/perl -w
use strict;
use Perceptron;  # ... or SubGradSVM

# SearnLabel.pl
# Author: Hal Daume III (me@hal3.name)
# See http://searn.hal3.name/

# Very simple implementation of the Searn algorithm for sequence
# labeling problems.  This implementation currently avoids the use of
# both *costing* and *weighted-all-pairs* by using a very simple
# multiclass perceptron implementation, currently relegated to the
# *Perceptron.pm* file.  This slightly worsens the results so that
# they do not match those in either my thesis or the Searn paper, but
# makes the algorithm much easier to understand.  A version that uses
# costing and WAP will be released soon.  We also exclusively use
# Hamming loss and the optimal policy approximation.

# File format: each line corresponds to one "word" in the input; the
# first column is the label, all the rest are features (assumed
# binary, sparse).  Blank lines separate "sentences."

my $filename = 'log.txt';
open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";

my $usage = "SearnLabel.pl [# iter] [beta] [train file] [test file]\n";

my $maxi = shift or die $usage;
my $beta = shift or die $usage;
my $trF  = shift or die $usage;
my $teF  = shift or die $usage;

# set up some variables; feel free to change these

my $NUMCLITERATIONS    = 10;          # run 5 perceptron passes per Searn iteration
my $RANDOMIZEORDER     = 1;          # set to 1 if you want the perceptron passes to be in random order
my $DOFEATURESELECTION = 0;          # set to 0 if you want to use all features

# first, load the training and test data

my ($X , $Y ) = loadFile($trF);
my ($Xt, $Yt) = loadFile($teF);

# $X = removeInfrequentFeatures($X);

# find all possible labels
my %allLabels = ();
for (my $n=0; $n<scalar @$Y; $n++) {
    for (my $m=0; $m<scalar @{$Y->[$n]}; $m++) {
        $allLabels{$Y->[$n][$m]} = 1;
    }
}

# create the weights

my %classifier = ();   # classifier{i} = classifier for the ith iteration
my %weight     = ();   # weight{i} = probability of calling classifier{i}

$classifier{0} = 'OPTIMAL POLICY';
$weight{0}     = 1;

# iterate
for (my $iter=1; $iter<=$maxi; $iter++) {
    print STDERR "it $iter\t";

    # create a classifier for this iteration
    my $w = new_classifier(\%allLabels);

    # run a few iterations of the perceptron
    for (my $cliter=1; $cliter<=$NUMCLITERATIONS; $cliter++) {
        print STDERR ".";
        # randomize the order of examples
        my @order = ();
        for (my $n=0; $n<scalar @$X; $n++) { $order[$n] = $n; }

        if ($RANDOMIZEORDER) {
            for (my $n=0; $n<scalar @$X; $n++) { 
                my $t = $order[$n];
                my $r = int(rand() * (scalar @$X-$n) + $n);
                $order[$n] = $order[$r];
                $order[$r] = $t;
            }
        }

        # for each example...
        for (my $nn=0; $nn<scalar @$X; $nn++) {
            my $n = $order[$nn];

            # decode according to current policy
            my $P = decode($X->[$n], $Y->[$n]);

            # create classification examples
            my $prev = '<s>';
            for (my $m=0; $m<scalar @{$X->[$n]}; $m++) {
                add_example($w, $Y->[$n][$m], $prev, $X->[$n][$m]);
                $prev = $P->[$m];
            }
        }
    }

    # reduce probability of calling old classifiers
    foreach my $i (keys %weight) {
        $weight{$i} *= (1 - $beta);
    }

    # add new classifier
    print STDERR "|";
    finalize_classifier($w);
    $weight{$iter} = $beta;
    $classifier{$iter} = $w;

    # get training loss
    my $numWrong = 0; my $total = 0;
    for (my $n=0; $n<scalar @$X; $n++) {
        my $P = decode($X->[$n]);
        for (my $m=0; $m<scalar @{$X->[$n]}; $m++) {
            $total++;
            if ($P->[$m] ne $Y->[$n][$m]) { $numWrong++; }
        }
    }

    print STDERR "\ttrain l=" . ($numWrong/$total);

    # now, apply to test data
    $numWrong = 0; $total = 0;
    for (my $n=0; $n<scalar @$Xt; $n++) {
        my $P = decode($Xt->[$n]);
        if($iter==$maxi) { print scalar @$P . "\n"; }
        for (my $m=0; $m<scalar @{$Xt->[$n]}; $m++) {
            # Print labels here
            if($iter==$maxi) { print $fh $P->[$m] . "\n"; }
            $total++;
            if ($P->[$m] ne $Yt->[$n][$m]) { $numWrong++; }
        }
        if($iter==$maxi){ print $fh "\n"; }
    }

    print STDERR "\ttest l=" . ($numWrong/$total) . "\n";
}

close $fh;

sub decode {
    my ($X, $Y) = @_;

    # if we can't use the optimal policy, we need to remove the chance
    # of calling it
    my $totalProbability = 1;
    if (not defined $Y) { $totalProbability -= $weight{0}; }

    # predict labels
    my @P = ();
    my $prev = '<s>';
    for (my $m=0; $m<scalar @$X; $m++) {
        # find which weight vector we'll use
        my $r = rand() * $totalProbability;
        my $c = -1;
        foreach my $i (keys %weight) {
            if ((not defined $Y) && ($i == 0)) { 
                # skip the optimal policy if we don't have it
                next;
            }
            if ($r < $weight{$i}) { $c = $i; last; }
            $r -= $weight{$i};
        }

        if (($c < 0) || (not defined $classifier{$c})) { 
            die "could not find classifier $c\n"; 
        }
        if ($c == 0) { # optimal policy step
            $P[$m] = $Y->[$m];
        } else {       # use classifier
            if (not defined $classifier{$c}) { die "classifier $c not found\n"; }
            $P[$m] = classify($classifier{$c}, $prev, \@{$X->[$m]});
        }
        $prev = $P[$m];
    }

    return \@P;
}


sub loadFile {
    my ($fn) = @_;

    my $N = 0;
    my $M = 0;
    my @X = ();
    my @Y = ();
    open F, $fn or die "could not open $fn\n";
    while (<F>) {
        chomp;
        if (/^[\s]*$/) {
            if ($M > 0) {
                $N++;
                $M = 0;
            }
            next;
        }

        my ($lab, @f) = split;

        $Y[$N][$M] = $lab;
        for (my $i=0; $i<@f; $i++) {
            $X[$N][$M][$i] = $f[$i];
        }
        $M++;
    }
    close F or die;

    return (\@X, \@Y);
}

sub removeInfrequentFeatures {
    my ($X) = @_;

    my %c = ();
    for (my $n=0; $n<scalar @$X; $n++) {
        for (my $m=0; $m<scalar @{$X->[$n]}; $m++) {
            for (my $i=0; $i<scalar @{$X->[$n][$m]}; $i++) {
                $c{$X->[$n][$m][$i]}++;
            }
        }
    }

    print STDERR ((scalar keys %c) . " total features");

    if ($DOFEATURESELECTION) {
        foreach my $f (keys %c) {
            if ($c{$f} <= 1) { delete $c{$f}; }
        }
    }

    print STDERR ", " . (scalar keys %c) . " retained\n";

    my @Xnew = ();

    for (my $n=0; $n<scalar @$X; $n++) {
        for (my $m=0; $m<scalar @{$X->[$n]}; $m++) {
            @{$Xnew[$n][$m]} = ();
            my $j = 0;
            for (my $i=0; $i<scalar @{$X->[$n][$m]}; $i++) {
                if (exists $c{$X->[$n][$m][$i]}) {
                    $Xnew[$n][$m][$j] = $X->[$n][$m][$i];
                    $j++;
                }
            }
        }
    }

    return \@Xnew;
}
