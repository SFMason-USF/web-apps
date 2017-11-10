require 'sinatra'
require './rsg.rb'

get '/' do
    open('index.html', 'r') { |f| f.read }
end

get '/:grammar' do
    rsg(params[:grammar])
end
