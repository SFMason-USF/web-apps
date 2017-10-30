# Extracts just the definitions from the grammar file
# Returns an array of strings where each string is the lines for
# a given definition (without the braces)
def read_grammar_defs(filename)
  filename = 'grammars/' + filename unless filename.start_with? 'grammars/'
  filename += '.g' unless filename.end_with? '.g'
  contents = open(filename, 'r') { |f| f.read }
  contents.scan(/{(.+?)}/m).map do |rule_array|
    rule_array[0]
  end
end

# Takes data as returned by read_grammar_defs and reformats it
# in the form of an array with the first element being the
# non-terminal and the other elements being the productions for
# that non-terminal.
# Remember that a production can be empty (see third example)
# Example:
#   split_definition "\n<start>\nYou <adj> <name> . ;\nMay <curse> . ;\n"
#     returns ["<start>", "You <adj> <name> .", "May <curse> ."]
#   split_definition "\n<start>\nYou <adj> <name> . ;\n;\n"
#     returns ["<start>", "You <adj> <name> .", ""]
def split_definition(raw_def)
  words = raw_def.split(/\n/, -1)
  words.each {|word|
    word.tr!(';', '')
    word.strip!
  }
  if words[0].empty?
    words.delete_at(0)
  end
  words.delete_at(-1)
  return words
end

# Takes an array of definitions where the definitions have been
# processed by split_definition and returns a Hash that
# is the grammar where the key values are the non-terminals
# for a rule and the values are arrays of arrays containing
# the productions (each production is a separate sub-array)

# Example:
# to_grammar_hash([["<start>", "The   <object>   <verb>   tonight."], ["<object>", "waves", "big    yellow       flowers", "slugs"], ["<verb>", "sigh <adverb>", "portend like <object>", "die <adverb>"], ["<adverb>", "warily", "grumpily"]])
# returns {"<start>"=>[["The", "<object>", "<verb>", "tonight."]], "<object>"=>[["waves"], ["big", "yellow", "flowers"], ["slugs"]], "<verb>"=>[["sigh", "<adverb>"], ["portend", "like", "<object>"], ["die", "<adverb>"]], "<adverb>"=>[["warily"], ["grumpily"]]}
def to_grammar_hash(split_def_array)
  myHash = Hash.new
  split_def_array.each {|x|
    myArray = Array.new
    x.each_with_index {|y, yi|
      unless yi == 0 || y.nil? || y == 0
        myArray.push(y.split(/\s+/))
      end
    }
    unless myArray.nil?
      myHash[x[0].gsub(/\s+/, '')] = myArray
    end
  }
  return myHash
end

# Returns true iff s is a non-terminal
# a.k.a. a string where the first character is <
#        and the last character is >
def is_non_terminal?(s)
  s.strip()
  return s[0] == '<' && s[-1] == '>'
end

# Given a grammar hash (as returned by to_grammar_hash)
# returns a string that is a randomly generated sentence from
# that grammar
#
# Once the grammar is loaded up, begin with the <start> production and expand it to generate a
# random sentence.
# Note that the algorithm to traverse the data structure and
# return the terminals is extremely recursive.
#
# The grammar will always contain a <start> non-terminal to begin the
# expansion. It will not necessarily be the first definition in the file,
# but it will always be defined eventually. Your code can
# assume that the grammar files are syntactically correct
# (i.e. have a start definition, have the correct  punctuation and format
# as described above, don't have some sort of endless recursive cycle in the
# expansion, etc.). The names of non-terminals should be considered
# case-insensitively, <NOUN> matches <Noun> and <noun>, for example.
def expand(grammar, non_term='<start>')
  # TODO: your implementation here
  non_term.downcase!
    template = grammar[non_term].sample() #pick a random template
    str = ""
    template.each { |term| str += (is_non_terminal?(term) ? expand(grammar, term) : term).strip + ' '}
    if non_term == "<start>"
      str.strip!
      str += ''
    end
  return str
end

# Given the name of a grammar file,
# read the grammar file and print a
# random expansion of the grammar
def rsg(filename)
	# defs = read_grammar_defs(filename)
	# split_defs = [split_definition(def) for def in defs]
	# hash = to_grammar_hash(split_defs)
	# generated_sentence = expand(hash)
	# print(generated_sentence)
	# --or--
  # print(expand(to_grammar_hash([split_definition(def) for def in read_grammar_defs(filename)])))
  defs = read_grammar_defs(filename)
  split_defs = defs.map { |d| split_definition(d) }
  hash = to_grammar_hash(split_defs)
  generated_sentence = expand(hash)
  puts(generated_sentence)
end

if __FILE__ == $0
  # prompt the user for the name of a grammar file
  # rsg that file
  puts 'Please enter the name of the grammar file: '
  STDOUT.flush
  gFile = gets().chomp
  rsg(gFile)
end
