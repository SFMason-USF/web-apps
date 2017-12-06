require 'sinatra'
require 'dm-core'
require 'dm-migrations'
require 'data_mapper'
require 'dm-sqlite-adapter'
require 'json'

DataMapper.setup(:default, "sqlite3://#{Dir.pwd}/names.db")

class MyNames
  include DataMapper::Resource
  property :name, String, :key => true
  property :val1, Integer
  property :val2, Integer
  property :val3, Integer
  property :val4, Integer
  property :val5, Integer
  property :val6, Integer
  property :val7, Integer
  property :val8, Integer
  property :val9, Integer
  property :val10, Integer
  property :val11, Integer
end

DataMapper.finalize
DataMapper.auto_upgrade!

# File.foreach('names-data.txt') do |line|
#   name, *values = line.split
#   params = {name: name.downcase}
#   values.each_with_index do |value, i|
#     params[:"val#{i+1}"] = value
#   end
#   MyNames.create params
# end

get '/' do
  open('index.html', 'r') { |f| f.read }
end

get '/names/:name' do |n|

  valid_chars = ('a'..'z').to_a
  n = n.downcase
  cond = n.chars.detect {|ch| !valid_chars.include?(ch)}.nil?
  if cond
    my_name = MyNames.get(n).name
    if my_name
      my_years = Array.new
      my_years.push(MyNames.get(n).val1)
      my_years.push(MyNames.get(n).val2)
      my_years.push(MyNames.get(n).val3)
      my_years.push(MyNames.get(n).val4)
      my_years.push(MyNames.get(n).val5)
      my_years.push(MyNames.get(n).val6)
      my_years.push(MyNames.get(n).val7)
      my_years.push(MyNames.get(n).val8)
      my_years.push(MyNames.get(n).val9)
      my_years.push(MyNames.get(n).val10)
      my_years.push(MyNames.get(n).val11)

      {:name => my_name, :ratings => my_years}.to_json
    end
  else "No entered names found"
  end
end