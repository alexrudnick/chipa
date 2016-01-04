# scorer_task3.pl for the Cross-Lingual Word Sense Disambiguation task SemEval 2010 
# by Els Lefever 19 January 2010
# Minor adaptation from code written by Diana McCarthy 
# for Cross-Lingual Lexical Substitution Task SemEval 2010

#changes Els 23 March 2010
# 1. line 322: change \w to . to accept accentuated Unicode characters
# 2. do lowercase conversion for evaluation because of different lemmatisation behavior
# 3. chomp lines in order to solve problems for windows saved files
# 4. changed check on number of guesses in oof evaluation

use strict;
use utf8; # 29/3/2010

my $batchpath = "/Users/elslefever/Doctoraat/SemEval_2010/Competition/Evaluation/sys/"; # "" for default

my $ansfile = shift(@ARGV);
my $goldfile = shift(@ARGV);
my $type =  shift(@ARGV);
my $scoretype = shift(@ARGV);
my $verbose = shift(@ARGV);


my $goldpath = "\."; ### Needed only for analysis

 top();


sub top {
if (!$ansfile || !$goldfile || ($ansfile =~ /-(t|v)$/) || ($goldfile =~ /-(t|v)/)) {
  print "score.pl usage: systemfile goldfile [-t best|oof] [-v]\n";
  undef $scoretype;
}

if (!$type) {
  $scoretype = 'best';
}
elsif (($type eq '-v') && !$scoretype && !$verbose) {
  $scoretype = 'best';
  $verbose = '-v';
}
elsif ($type && ($type ne '-t')) {
  print "score.pl usage: systemfile goldfile [-t best|oof] [-v]\n";
  undef $scoretype;
}

###### used for analysis in 2007. 
my $subana; 
           # NMWS only using single word substitutes from GS
my $E = 1; # exclude,  all or MAN
           # 0 for RAND

my @ansf;
my $outf;
if ($ansfile eq "batch") {
    @ansf = dirfilespatt($batchpath,"$scoretype\$");
}
else {
    push(@ansf,$ansfile);
}

foreach $ansfile (@ansf) {
    open(RES,">$ansfile.results");    
    if ($scoretype) {
	if ($scoretype eq 'best') {
	    print RES "Scoring 'best' goldfile = $goldfile sysfile = $ansfile\n"; 
	    scorebest($goldfile,$ansfile,$subana,$E); # supplying best answers
	    #   $subana = 'NMWS';
	    #   print  "\nFURTHER ANALYSIS Scoring using only single word substitutes\n";
	    #   scorebest($goldfile,$ansfile,$subana,$E); 
	}
	elsif ($scoretype eq 'oof') {
	    print RES "Scoring 'oof' goldfile = $goldfile sysfile = $ansfile\n"; 
	    scoreoof($goldfile,$ansfile,$subana,$E); #supplying up to 10 answers
    
	    #   $subana = 'NMWS';
	    #   print  "\nFURTHER ANALYSIS Scoring using only single word substitutes\n";
	    #   scoreOOT($goldfile,$ansfile,$subana,$E); #supplying up to 10 answers
	}
	elsif ($scoretype) {
	    print RES "score.pl usage: systemfile goldfile [-t best|oot] [-v]\n";
	}
    }
    close(RES);
}
}

sub scorebest {
  my($goldfile,$ansfile,$subana,$E) = @_;
  my(%idws,%idres,%idmodes);
  my($line,$id,$wpos,$res,@res,$numguesses,$hu,$totmodatt,$besteqmode,$noCount,%notCount);
  my($totitems,$idcorr,$corr,$precision,$recall,$totmodes,$itemsattempted);
  my($sub,%norms,%done,$score,$posthoc);
  my $dp = 2;
  my $lcnt = 0;
  ($totitems,$totmodes) = readgoldfile($goldfile,\%idws,\%idres,\%idmodes,\%notCount,$subana,$E);
  open(SYS,$ansfile);
  while ($line = <SYS>) {
 	$line =~ s/\s+$//;
     	$line = lc($line); # 29/3/2010
    $lcnt++;    
    undef $idcorr;
    undef %norms;
    if ($line =~ /([\w.]+) (\S+) \:\: (.*)/) {
      $id = $2;
      $wpos = $1;
      $res = $3; 
      $res =~ s/;$//;# 29/3/2010 trailing ; removed
      #print "debug: LINE: $id $hu\n";
      $hu = sumvalues(\%{$idres{$id}});
            	$noCount = $notCount{$id};
            	$hu = $hu - $noCount;

      normalisevalues(\%{$idres{$id}},\%norms,$hu,$noCount);
      if ($hu && !$done{$id}) { # duplicates in system file
	$done{$id} = 1;
	if ($res =~ /\S/) {
	    @res = split(';',$res); # can't do on spaces because of MWEs
	    @res = fixmisc($subana,@res); # hypens, american british, apost
	    $numguesses = $#res + 1;
	    if ($numguesses) {
		$itemsattempted++;
	    }

	}
	else {
	   # print "$id $res DEBUG\n";
	}
	if ($idmodes{$id} && $numguesses) {
	  $totmodatt++;
	  if ($idmodes{$id} eq $res[0]) {
	    $besteqmode++;
	    if ($verbose) {
	      print RES "$wpos Item $id mode '$idmodes{$id}' : system '$res[0]'  correct\n";
	    }
	  }
	  elsif ($verbose) {
	      print RES "$wpos Item $id mode '$idmodes{$id}' : system '$res[0]' wrong\n";
	    }
	}
	foreach $sub (@res) {
	  $idcorr += $norms{$sub}; 
      }        
	  if ($idcorr) {
	    $score = (($idcorr / $numguesses)); 
	    $corr += $score;
	  }
	if ($verbose && $numguesses) {
	  print RES "$wpos Item $id credit $idcorr guesses $numguesses human responses $hu: score is $idcorr\n";
	}

    }
      else {
	 # print "not attempted $line\n"; # debugging items not included
      }
    } # item
    elsif ($line =~ /\S/) {
       print RES "Error in $ansfile on line $lcnt\n";
    }    
}
  $precision = $corr / $itemsattempted;
  $precision = myround($precision,$dp);
  $recall = $corr / $totitems;
  $recall = myround($recall,$dp);
  print RES "Total = $totitems, attempted = $itemsattempted\n";
  print RES "precision = $precision, recall = $recall\n";
  $precision = $besteqmode / $totmodatt; # where there was a mode and system had an answer
  $precision = myround($precision,$dp);
  $recall = $besteqmode / $totmodes;
  $recall = myround($recall,$dp);
  print RES "Total with mode $totmodes attempted $totmodatt\n";
  print RES "Mode precision = $precision, Mode recall = $recall\n";
  close(SYS);
}

sub scoreoof {
  my($goldfile,$ansfile,$subana,$E) = @_;
  my(%idws,%idres,%idmodes);
  my($line,$id,$wpos,$res,@res,$numguesses,$hu,$totmodatt,$foundmode,$noCount,%notCount);
  my($totitems,$idcorr,$corr,$precision,$recall,$totmodes,$itemsattempted);
  my($sub,%norms,%done,$score);
  my $dp = 2;
  my $lcnt = 0;
  my $dupflag = 0;
  ($totitems,$totmodes) = readgoldfile($goldfile,\%idws,\%idres,\%idmodes,\%notCount,$subana,$E);
  open(SYS,$ansfile);
  while ($line = <SYS>) {
     	$line =~ s/\s+$//;
	$line = lc($line); # 29/3/2010
      $lcnt++;
      undef $idcorr;
      undef %norms;
      if ($line =~ /([\w.]+) (\S+) \:\:\: (.*)/) { 
	  $id = $2;
	  $wpos = $1;
	  $res = $3;
	  $res =~ s/;$//;# 29/3/2010 trailing ; removed
	  $hu = sumvalues(\%{$idres{$id}});
      		$noCount = $notCount{$id};
      		$hu = $hu - $noCount;
	  normalisevalues(\%{$idres{$id}},\%norms,$hu);
      if ($hu && !$done{$id}) {
	$done{$id} = 1;
	if ($res =~ /\S/) {
	  @res = split(';',$res); # can't do on spaces because of MWEs
	  @res = fixmisc($subana,@res); # hypens, american british, apost
	  if ($#res > -1) {
	      $itemsattempted++;
	  }
	  if (duplicates_p(@res)) {
	      $dupflag++;
	      if ($verbose) {
		  print RES "NB duplicate at $wpos $id responses @res\n";
	      }
	  }
	}
	else {
	#    print "$id $res\n";
	}
	if ($#res > 4) {
	  @res = @res[0..4];
	  if ($verbose) {
	    print RES "$wpos Item $id exceeded 5 guesses\n";
	  }
	}
	if ($idmodes{$id} && ($#res > -1)) {
	  $totmodatt++;
	  if (strmember($idmodes{$id},@res)) {
	    $foundmode++; # mode is in guesses	    
	    if ($verbose) {
	      print RES "$wpos Item $id mode '$idmodes{$id}'  found in guesses\n";
	    }
	  }
	  elsif ($verbose) {
	      print RES "$wpos Item $id mode '$idmodes{$id}'  not found\n";
	    }
	}
	foreach $sub (@res) {
	  $idcorr += $norms{$sub}; 
	}      
	if ($idcorr) {
	  $corr += $idcorr; 
	}	
	if ($verbose &&  ($#res > -1)) {
	  print RES "$wpos Item $id credit $idcorr human responses $hu: score is $idcorr\n";
	}
      } # if $hu, humans said something
    } # item
    elsif ($line =~ /\S/) { 
      print RES "Error in $ansfile on line $lcnt\n";
    }    
  }
  if ($dupflag) {
      print RES "NB OOF file contains duplicates on $dupflag lines\n";
  }
  $precision = $corr / $itemsattempted;
  $precision = myround($precision,$dp);
  $recall = $corr / $totitems;
  $recall = myround($recall,$dp);
  print RES "Total = $totitems, attempted = $itemsattempted\n";
  print RES "precision = $precision, recall = $recall\n";
  $precision = $foundmode / $totmodatt; # where there was a mode and
                         # system had an answer
  $precision = myround($precision,$dp);
  $recall = $foundmode / $totmodes;
  $recall = myround($recall,$dp);
  print RES "Total with mode $totmodes attempted $totmodatt\n";
  print RES "precision = $precision, recall = $recall\n";
  close(SYS);
}





sub fixmisc {
  my($sa,@ans) = @_;
  my ($item,@result,$debug);
  foreach $item (@ans) {     
   if (($sa eq 'NMWS') && ($item =~ /\S \S/)) {# don't include MW subs 
       $debug .= "$item;";
   }
   else  {
    push(@result,$item);
   }
}
  return @result;
}

# gives ids (mws) or wpos to exclude from scoring
# this code was used for further analysis in 2007
sub subset {
    my($subana) = @_;
    my(%result);
    if ($subana =~  /RAND|MAN/) {
	%result = getman("$goldpath/MRsamples");
    }
    return %result;

}
sub getman {
    my($file) = @_;
    my($line,%result);
    open(SUB,"$file");
    while ($line = <SUB>) {
	if ($line =~ /(\w+);(\w)\.man/) {	    
	    $result{"$1\.$2"} = 1;
	}
    }
    close(SUB);
    return %result;
}



# $E was used for analyses in 2007
# set E as 1 if want to exclude  subset, or evaluate all
# set E as 0 if want to only use subset (for MAN)
sub readgoldfile {
  my($gsfile,$idwarr,$resarr,$modes,$notCount,$subana,$E) = @_;
  my($line,$id,$wpos,$rest,@res,$sub,$num,$mode,$modenum,$i,$totitems,$totmodes,%notCount);
  my($res,$ms,$first,%exclude);
  %exclude = subset($subana);
  open(GS,"$gsfile");
  while ($line = <GS>) {
	$line =~ s/\s+$//;
      	$line = lc($line); # 29/3/2010
    if ($line =~ /([\w.]+) (\S+) \:\: (.*)/) {
      $id = $2;
      $wpos = $1;
      $rest = $3;
       $rest =~ s/;$//; # 29/3/2010 trailing ; removed
      undef $mode;
      undef $modenum;
      undef $ms;
      undef $num;
      # !$E && $exclude{$wpos} MAN - use just these
      # $E and nothing in %exclude - use all
      # $E and !$exclude{$id} - not one of MWs we are ignoring
      #  $E and !$exclude{$wpos} - not one of manuals we are ignoring (i.e. RAND set)
      if(($E && (!$exclude{$id} && !$exclude{$wpos})) || (!$E && $exclude{$wpos})) { # mw ids, man rand are wpos
	  @res = split(';',$rest);
	  @res = removeifpatt('pn',@res); # 
	  if ($subana eq 'NMWS') { # not MWs as substitutes
	      @res = removeifpatt('\s\S+\s+\d+',@res);
	  }
	  $first = $res[0];
	#  if ($first =~ /[\w\'-\s]+ (\d+)/) {
	      if ($first =~ /.+ (\d+)/) { # 23/9/2010
		  #if ($first =~ /[.]+ (\d+)/) {
	      $num = $1;
	  }
	  if (($#res > 0) || ($num > 1)) { # i.e. 2 or morenon nil and non pn (proper noun)
	      if($num != "0"){
	      $totitems++;
	      }
	      $$idwarr{$id} = $wpos;
	      foreach $res (@res) {
		  if ($res =~ /(.+) (\d+)/) {
		      $sub = $1;
		      $num = $2;
		      # Els: added compound parts are not counted in number of gold standard guesses
		      # and get default score of "1" because are valid translations as well
		      
		      if($num == "0"){
		      $$notCount{$id}++;
		      }
			
		      
		      $sub =~ s/'//;# remove apostrophe, should only be one
		      if (!$mode) { # cond below will take care of those of 1
			  $mode = $sub;	  
			  $modenum = $num;
			  $$modes{$id} = $mode;	 
			  $totmodes++;

		      }
		      elsif (!$ms && $mode && ($num == $modenum)) { # mode found was not the most freq	  
			  delete $$modes{$id};	 
			  $totmodes--;
			  $ms = 1; # so we don't do this twice for 1 id

		      }
		      if($num == "0"){
		      $num = 1;
		      }
			#print "DEBUG: $id $sub $num\n";

		      $$resarr{$id}{$sub} = $num;
		  }	 
	      }      
	  }
      else {
	  print "can't use: $line\n"; # debugging
      }

  }# is part of group we are scoring
      else {
	  #print "not in group: $line\n"; # debugging
      }
  } # matches line
  else {
      #print "GS mismatch: $line\n"; # debugging
  }
} # while
  close(GS);

  return ($totitems,$totmodes);
}



###  utilities
sub removeifpatt {
	my($patt,@list) = @_;
	my($i,@result);
	foreach $i (@list) {
		if ($i !~ /$patt/) {
			push(@result,$i);
		}
	}	
	return @result;
}

# rounds by $db decimal places
sub myround {
    my($number,$dp) = @_;
	my($mult,$result,$dec,$len,$dpo,$diff);
    $number *= 100; # to give percentages
	$dpo = '0' x $dp;
	$mult = 1 . $dpo;
	$number = $number * $mult;
    	$result =  int($number + .5);
	$result = $result /  $mult;
	if ($result =~ /\.(\d+)/) {
		$dec = $1;
		$len = length($dec);
		$diff = $dp - $len;
		while ($diff) {
			$result .= '0';
			$diff--;
		}
	}
	else {
		$result .= ".$dpo";
	}
	return $result;
}


sub sumvalues {
    my($array) = @_;
    my($key,$val,$result);
    while (($key,$val) = each %$array) {
        $result += $val;
    }
    return $result;
}


# normalise by sum, and account for hyphens  in GS
# so if humans put hyphens, then could be spaces or hyphens
# but if humans didn't and systems do systems may be found incorrect
# hypens an issue for 2007 but not in spanish data
sub normalisevalues {
  my($source,$target,$sum,$not) = @_;
  my($key,$val,$key2,$result);
  while (($key,$val) = each %$source) {
        $$target{$key} = $val / $sum;
        	 # print STDERR "$key $val $sum\n";
	if ($key =~ /-/) {
	  $key2 = $key;
	  $key2 =~ s/-/ /g;
	  $$target{$key2} = $val / $sum;
	}
    }
}


sub strmember {
    my($item,@list) = @_;
    my($index);
    for ($index = 0; $index <= $#list; $index++) {
        if ($list[$index] eq $item) {
            return $index + 1;
            last;
        }
    }
}



# get all files from a directory
sub dirfiles {
	my($path) = @_;
	my(@files);
        opendir(DIR,"$path");
	@files = grep(!/^\.\.?$/, readdir(DIR));
        closedir(DIR);
	return @files;
}


sub dirfilespatt {
	my($path,$patt) = @_;
	my(@files,$file,@result);
	@files = dirfiles($path);
	foreach $file (@files) {
		if ($file =~ /$patt/) {
			push(@result,"$path/$file");
		}
	}
	return @result;

}

sub removeall {
        my($item,@list) = @_;
        my($i,@result);
        foreach $i (@list) {
                if ($i ne $item) {
                        push(@result,$i);
                }
        }
        return @result;
}




sub printinfile {
	my($array,$file) = @_;
	my($key,@keys);
	open(PSBVFILE,">>$file");
	@keys = keys %$array;
	foreach $key (@keys) {
	    print PSBVFILE "$key  $$array{$key}\n\n"
	}
	close(PSBVFILE);

}

sub duplicates_p {
	my(@list) = @_;
	my($i);
	for($i = 0; $i <= $#list; $i++) {
        	if (strmember($list[$i],@list[$i+1..$#list])) {
            		return 1;
        	} #if
    	} # for
    	return 0;
}
