# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ushahar/CLionProjects/ex3B_ushahar

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ushahar/CLionProjects/ex3B_ushahar/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/ex3B_ushahar.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/ex3B_ushahar.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/ex3B_ushahar.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/ex3B_ushahar.dir/flags.make

CMakeFiles/ex3B_ushahar.dir/linked_list.c.o: CMakeFiles/ex3B_ushahar.dir/flags.make
CMakeFiles/ex3B_ushahar.dir/linked_list.c.o: ../linked_list.c
CMakeFiles/ex3B_ushahar.dir/linked_list.c.o: CMakeFiles/ex3B_ushahar.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ushahar/CLionProjects/ex3B_ushahar/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/ex3B_ushahar.dir/linked_list.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/ex3B_ushahar.dir/linked_list.c.o -MF CMakeFiles/ex3B_ushahar.dir/linked_list.c.o.d -o CMakeFiles/ex3B_ushahar.dir/linked_list.c.o -c /home/ushahar/CLionProjects/ex3B_ushahar/linked_list.c

CMakeFiles/ex3B_ushahar.dir/linked_list.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/ex3B_ushahar.dir/linked_list.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/ushahar/CLionProjects/ex3B_ushahar/linked_list.c > CMakeFiles/ex3B_ushahar.dir/linked_list.c.i

CMakeFiles/ex3B_ushahar.dir/linked_list.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/ex3B_ushahar.dir/linked_list.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/ushahar/CLionProjects/ex3B_ushahar/linked_list.c -o CMakeFiles/ex3B_ushahar.dir/linked_list.c.s

CMakeFiles/ex3B_ushahar.dir/markov_chain.c.o: CMakeFiles/ex3B_ushahar.dir/flags.make
CMakeFiles/ex3B_ushahar.dir/markov_chain.c.o: ../markov_chain.c
CMakeFiles/ex3B_ushahar.dir/markov_chain.c.o: CMakeFiles/ex3B_ushahar.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ushahar/CLionProjects/ex3B_ushahar/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/ex3B_ushahar.dir/markov_chain.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/ex3B_ushahar.dir/markov_chain.c.o -MF CMakeFiles/ex3B_ushahar.dir/markov_chain.c.o.d -o CMakeFiles/ex3B_ushahar.dir/markov_chain.c.o -c /home/ushahar/CLionProjects/ex3B_ushahar/markov_chain.c

CMakeFiles/ex3B_ushahar.dir/markov_chain.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/ex3B_ushahar.dir/markov_chain.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/ushahar/CLionProjects/ex3B_ushahar/markov_chain.c > CMakeFiles/ex3B_ushahar.dir/markov_chain.c.i

CMakeFiles/ex3B_ushahar.dir/markov_chain.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/ex3B_ushahar.dir/markov_chain.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/ushahar/CLionProjects/ex3B_ushahar/markov_chain.c -o CMakeFiles/ex3B_ushahar.dir/markov_chain.c.s

CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.o: CMakeFiles/ex3B_ushahar.dir/flags.make
CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.o: ../tweets_generator.c
CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.o: CMakeFiles/ex3B_ushahar.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ushahar/CLionProjects/ex3B_ushahar/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.o -MF CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.o.d -o CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.o -c /home/ushahar/CLionProjects/ex3B_ushahar/tweets_generator.c

CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/ushahar/CLionProjects/ex3B_ushahar/tweets_generator.c > CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.i

CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/ushahar/CLionProjects/ex3B_ushahar/tweets_generator.c -o CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.s

# Object files for target ex3B_ushahar
ex3B_ushahar_OBJECTS = \
"CMakeFiles/ex3B_ushahar.dir/linked_list.c.o" \
"CMakeFiles/ex3B_ushahar.dir/markov_chain.c.o" \
"CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.o"

# External object files for target ex3B_ushahar
ex3B_ushahar_EXTERNAL_OBJECTS =

ex3B_ushahar: CMakeFiles/ex3B_ushahar.dir/linked_list.c.o
ex3B_ushahar: CMakeFiles/ex3B_ushahar.dir/markov_chain.c.o
ex3B_ushahar: CMakeFiles/ex3B_ushahar.dir/tweets_generator.c.o
ex3B_ushahar: CMakeFiles/ex3B_ushahar.dir/build.make
ex3B_ushahar: CMakeFiles/ex3B_ushahar.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ushahar/CLionProjects/ex3B_ushahar/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking C executable ex3B_ushahar"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/ex3B_ushahar.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/ex3B_ushahar.dir/build: ex3B_ushahar
.PHONY : CMakeFiles/ex3B_ushahar.dir/build

CMakeFiles/ex3B_ushahar.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/ex3B_ushahar.dir/cmake_clean.cmake
.PHONY : CMakeFiles/ex3B_ushahar.dir/clean

CMakeFiles/ex3B_ushahar.dir/depend:
	cd /home/ushahar/CLionProjects/ex3B_ushahar/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ushahar/CLionProjects/ex3B_ushahar /home/ushahar/CLionProjects/ex3B_ushahar /home/ushahar/CLionProjects/ex3B_ushahar/cmake-build-debug /home/ushahar/CLionProjects/ex3B_ushahar/cmake-build-debug /home/ushahar/CLionProjects/ex3B_ushahar/cmake-build-debug/CMakeFiles/ex3B_ushahar.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/ex3B_ushahar.dir/depend

