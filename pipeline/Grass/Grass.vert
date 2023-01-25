#version 400

//inputs
layout (location=0) in vec3 position;
layout (location=1) in vec2 attr_textureCoord;

//uniforms
uniform mat4x4 MVP;
uniform float time;
uniform float dist;
uniform float size;
uniform float speed;
uniform float max_height;
uniform sampler2D displacement;
uniform sampler2D heightMap;
uniform int collumn;

//outputs
out float age;
out float height;
out vec2 textureCoord;

//noise texture sampler function responsible for introducing slight randomness to the calculation
float noise(vec2 source){
    float frequency = 0.07;
    float amplitude = 0.0005;
    vec2 result = source+(texture(displacement,source*time*frequency)).xy*amplitude;
    return result.x-result.y;
}

//oscilator responsible for creating the effect of wind
vec3 oscilate(vec3 worldPlacement){
    vec3 result;
    result.x =  position.y*(sin(speed*(noise(worldPlacement.xz)+time)/4))/2;
    result.y =  position.y*(sin(speed*(noise(worldPlacement.xz)+time)/4))/2;
    result.z =  position.y*(sin(speed*(noise(worldPlacement.xz)+time)/4))/2;
    return result;
}

//2D vector randomizer using a sampled white noise texture
vec2 rand(vec2 UV){
    vec4 color = texture(displacement,UV);
    return vec2(color.x+color.z-1,(color.y-color.z)*2-1);
}

//samples the height map buffering it's color and then calculates it's brightness to be added to the y coordinate (height of the terrain)
float heightMapper(vec2 center,vec3 coord){
    vec4 buffered_color = texture(heightMap,(coord.xz+center)/(4*size));
    return (size/4)*(buffered_color.x+buffered_color.y+buffered_color.z)/3;
}

void main(){

    // calculates the height between 1 and 0 to pass what sction of the grass blade is being rendered (this controls coloring in fragment shader)
    height = position.y/max_height;

    // initializes coordinates on the base position of the 3D model
    vec3 coord=position;

    // calculates the array coordinates based on it's instance ID and number of collumns
    vec2 arrayPos = vec2(gl_InstanceID-floor(gl_InstanceID/collumn)*collumn,(floor(gl_InstanceID/collumn)));

    // trick function to vary grass age (1 to 3), grouping older grass together in packs
    age = (2-cos((pow(arrayPos.x+10,2)-pow(arrayPos.y+10,2))/10));

    // spreads the grass blades according to their array position and distancing between each other
    coord.xz += arrayPos*dist;
    
    // samples a white noise texture to displace the world coordinates of the grass blade based on the pixel color of the texture scaled by the distancing between each blade on the array
    coord.xz += rand(arrayPos/10)*dist;
    
    // scales the length of the grass based on the age multiplyer(1 to 3)
    coord.y = coord.y*age;

    // centers grass field on the origin point (0,0,0)
    coord.xz -= collumn*dist/2;
    
    // oscilation mimics wind taking into consiration the absolute length of the grass blade and the age scaling
    coord += oscilate(coord);

    //geographical distortion
    coord.y += heightMapper(vec2(-size/2,-size/2),coord);

    //finalizes the position based on the MVP matrix and finalized coordinates
    gl_Position = MVP * vec4(coord,1.0);
}