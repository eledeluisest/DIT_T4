use Lingua::EN::Tagger;

# Create a parser object
my $p = new Lingua::EN::Tagger;
my $fin = "TEST.txt";
open(TEXTO,'<', $fin);

# Add part of speech tags to a text
my $fout = "LINGUATAGGERTEST.txt";
open(FH, '>', $fout) or die $!;
close(FH);
while(<TEXTO>){

my $tagged_text = $p->add_tags($_); 
# Get a readable version of the tagged text
my $readable_text = $p-> get_readable($_);


open(FH, '>>', $fout) or die $!;
print FH $readable_text;
close(FH);
}
close(TEXTO);




