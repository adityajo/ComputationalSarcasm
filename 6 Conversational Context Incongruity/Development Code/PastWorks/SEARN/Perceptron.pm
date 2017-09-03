1;

sub new_classifier {
    my ($L) = @_;     # this should be a hash of all possible labels

    my %c = ();

    %{$c{W}} = ();    # actual weights
    %{$c{A}} = ();    # averaged weights
    $c{C}    = 1;     # averaging count

    foreach my $l (keys %$L) {
        $c{L}{$l} = 1;
        %{$c{W}{$l}} = ();
        %{$c{A}{$l}} = ();
    }

    return \%c;
}


sub add_example {
    my ($c, $y, $prev, $X) = @_;    # y = true, prev = previous label, X = features

    # first, predict
    my %p = ();
    foreach my $l (keys %{$c->{L}}) {
        $p{$l} = 0;
        foreach my $f (@$X) {
            $p{$l} += $c->{W}{$l}{$f        } if defined $c->{W}{$l}{$f};
            $p{$l} += $c->{W}{$l}{"$prev $f"} if defined $c->{W}{$l}{"$prev $f"};
        }
    }

    # first highest scoring label
    my ($bestL) = keys %p;
    foreach my $l (keys %p) {
        if ($p{$l} > $p{$bestL}) { $bestL = $l; }
    }

    # if wrong, update
    if ($bestL ne $y) {
        foreach my $f (@$X) {
            $c->{W}{$y}{$f        } += 1;
            $c->{W}{$y}{"$prev $f"} += 1;
            $c->{A}{$y}{$f        } += $c->{C};
            $c->{A}{$y}{"$prev $f"} += $c->{C};

            $c->{W}{$bestL}{$f        } -= 1;
            $c->{W}{$bestL}{"$prev $f"} -= 1;
            $c->{A}{$bestL}{$f        } -= $c->{C};
            $c->{A}{$bestL}{"$prev $f"} -= $c->{C};
        }
    }
    $c->{C}++;
}


sub finalize_classifier {
    my ($c) = @_;

    # explicitly compute averaged wiehgts
    foreach my $l (keys %{$c->{L}}) {
        foreach my $f (keys %{$c->{W}{$l}}) {
            $c->{F}{$l}{$f} = $c->{W}{$l}{$f} - $c->{A}{$l}{$f} / $c->{C};
        }
    }
}


sub classify {
    my ($c, $prev, $X) = @_;

    # first, predict
    my %p = ();
    foreach my $l (keys %{$c->{L}}) {
        $p{$l} = 0;
        foreach my $f (@$X) {
            $p{$l} += $c->{W}{$l}{$f        } if defined $c->{W}{$l}{$f};
            $p{$l} += $c->{W}{$l}{"$prev $f"} if defined $c->{W}{$l}{"$prev $f"};
        }
    }

    # first highest scoring label
    my ($bestL) = keys %p;
    foreach my $l (keys %p) {
        if ($p{$l} > $p{$bestL}) { $bestL = $l; }
    }

    return $bestL;
}
