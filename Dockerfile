# syntax=docker/dockerfile:1
FROM ruby:2.7.2
RUN apt-get update -qq && apt-get install -y nodejs postgresql-client
WORKDIR /test-interview-question-master
COPY Gemfile /test-interview-question-master/Gemfile
COPY Gemfile.lock /test-interview-question-master/Gemfile.lock
COPY . /test-interview-question-master
RUN gem install bundler:1.16.1
RUN bundle install

# Add a script to be executed every time the container starts.
#COPY entrypoint.sh /usr/bin/

#RUN bin/rails server
EXPOSE 3000



# Configure the main process to run when running the image
CMD ["bin/rails", "server", "-b", "0.0.0.0"]
