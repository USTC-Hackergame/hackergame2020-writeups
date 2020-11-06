cmake_minimum_required(VERSION 3.0.0)
project(glHackergame VERSION 0.1.0)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules/")

if(WIN32)
	set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)
endif(WIN32)

link_directories(${CMAKE_SOURCE_DIR}/lib)

set(CMAKE_CXX_STANDARD_REQUIRED 17)

# find the required packages
find_package(GLM REQUIRED)
message(STATUS "GLM included at ${GLM_INCLUDE_DIR}")
find_package(GLFW3 REQUIRED)
message(STATUS "Found GLFW3 in ${GLFW3_INCLUDE_DIR}")
find_package(ASSIMP REQUIRED)
message(STATUS "Found ASSIMP in ${ASSIMP_INCLUDE_DIR}")


if(WIN32)
  set(LIBS glfw3 opengl32 assimp)
elseif(UNIX AND NOT APPLE)
  set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -Wall")
  find_package(OpenGL REQUIRED)
  add_definitions(${OPENGL_DEFINITIONS})
  find_package(X11 REQUIRED)
  # note that the order is important for setting the libs
  # use pkg-config --libs $(pkg-config --print-requires --print-requires-private glfw3) in a terminal to confirm
  set(LIBS ${GLFW3_LIBRARY} X11 Xrandr Xinerama Xi Xxf86vm Xcursor GL dl pthread freetype ${ASSIMP_LIBRARY})
  set (CMAKE_CXX_LINK_EXECUTABLE "${CMAKE_CXX_LINK_EXECUTABLE} -ldl")
elseif(APPLE)
  INCLUDE_DIRECTORIES(/System/Library/Frameworks)
  FIND_LIBRARY(COCOA_LIBRARY Cocoa)
  FIND_LIBRARY(OpenGL_LIBRARY OpenGL)
  FIND_LIBRARY(IOKit_LIBRARY IOKit)
  FIND_LIBRARY(CoreVideo_LIBRARY CoreVideo)
  MARK_AS_ADVANCED(COCOA_LIBRARY OpenGL_LIBRARY)
  SET(APPLE_LIBS ${COCOA_LIBRARY} ${IOKit_LIBRARY} ${OpenGL_LIBRARY} ${CoreVideo_LIBRARY})
  SET(APPLE_LIBS ${APPLE_LIBS} ${GLFW3_LIBRARY} ${ASSIMP_LIBRARY})
  set(LIBS ${LIBS} ${APPLE_LIBS})
else()
  set(LIBS )
endif(WIN32)

# first create relevant static libraries requried for other projects

add_library(GLAD "main/glad.c")
set(LIBS ${LIBS} GLAD)

add_executable(glHackergame main/glHackergame.cpp)
target_link_libraries(glHackergame ${LIBS})

add_executable(converter util/converter.cpp)
target_link_libraries(converter assimp)

set(TARGETS glHackergame converter)

foreach(TGT_NAME ${TARGETS})
    if(WIN32)
        set_target_properties(${TGT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/")
        set_target_properties(${TGT_NAME} PROPERTIES VS_DEBUGGER_WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/Debug")
    elseif(UNIX AND NOT APPLE)
        set_target_properties(${TGT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/")
    elseif(APPLE)
        set_target_properties(${TGT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/")
        set_target_properties(${TGT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG "${CMAKE_SOURCE_DIR}/bin/")
        set_target_properties(${TGT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_SOURCE_DIR}/bin/")
    endif(WIN32)
endforeach(TGT_NAME)

file(GLOB SHADERS
    "main/*.vs"
    "main/*.fs"
    "main/*.bin"
)
foreach(SHADER ${SHADERS})
    if(WIN32)
        # configure_file(${SHADER} "test")
        add_custom_command(TARGET glHackergame PRE_BUILD COMMAND ${CMAKE_COMMAND} -E copy ${SHADER} $<TARGET_FILE_DIR:glHackergame>)
    elseif(UNIX AND NOT APPLE)
        file(COPY ${SHADER} DESTINATION ${CMAKE_SOURCE_DIR}/bin/)
    elseif(APPLE)
        # create symbolic link for *.vs *.fs *.gs
        get_filename_component(SHADERNAME ${SHADER} NAME)
        makeLink(${SHADER} ${CMAKE_SOURCE_DIR}/bin/${SHADERNAME} glHackergame)
    endif(WIN32)
endforeach(SHADER)

include_directories(${CMAKE_SOURCE_DIR}/includes)