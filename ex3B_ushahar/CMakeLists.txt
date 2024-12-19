cmake_minimum_required(VERSION 3.22)
project(ex3B_ushahar C)

set(CMAKE_C_STANDARD 99)

add_executable(ex3B_ushahar
        linked_list.c
        markov_chain.c
        tweets_generator.c)
