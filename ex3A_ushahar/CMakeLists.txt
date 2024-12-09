cmake_minimum_required(VERSION 3.22)
project(ex3A_ushahar C)

set(CMAKE_C_STANDARD 99)

add_executable(ex3A_ushahar
        linked_list.c
        tweets_generator.c
        markov_chain.c
)
