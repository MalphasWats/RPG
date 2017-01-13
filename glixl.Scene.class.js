/* Scene Class */
var glixl = (function(glixl)
{
    glixl.Scene = function Scene(parameters)
    {
        if (!parameters.context)
            throw new Error("*** GLIXL ERROR: No gl context provided to Scene");
            
        this.context = parameters.context;
        
        this.sprite_sheet = parameters.sprite_sheet || new glixl.SpriteSheet({context: this.context});
        
        this.sprites = [];
        this.tiles = [];
        
        this.width = parameters.width || 400;
        this.height = parameters.height || 400;
        
        this.tile_size = parameters.tile_size || {width: 16, height:16};
        
        this.columns = Math.floor(this.width / this.tile_size.width);
        this.rows = Math.floor(this.height / this.tile_size.height);
        
        this.viewport = {
            x: 0,
            y: 0,
            width:  this.width,
            height: this.height,
            max_x: 0,
            max_y: 0
        };
        
        this.viewport_matrix = [
            1,  0, 0, 0,
            0,  1, 0, 0,
            0,  0, 1, 0,
            -this.viewport.x, -this.viewport.y, 0, 1,
        ];
        
        this.projection_matrix = [
            2 / this.viewport.width, 0, 0, 0,
            0, -2 / this.viewport.height, 0, 0,
            0, 0, 2 / this.viewport.height, 0,
            -1, 1, 0, 1,
        ];
        
        // create buffers
        this.tile_vertex_buffer = this.context.createBuffer();
        this.tile_texture_buffer = this.context.createBuffer();
        
        this.sprite_vertex_buffer = this.context.createBuffer();
        this.sprite_texture_buffer = this.context.createBuffer();
        
        this.viewport_uniform = this.context.getUniformLocation(this.context.program, "viewport_matrix");
        this.projection_uniform = this.context.getUniformLocation(this.context.program, "projection_matrix");
        
        this.position_attribute = this.context.getAttribLocation(this.context.program, "a_position");
        this.context.enableVertexAttribArray(this.position_attribute);
        
        this.texture_attribute = this.context.getAttribLocation(this.context.program, "a_texCoords");
        this.context.enableVertexAttribArray(this.texture_attribute);
        
        this.tile_vertex_coords = [];
        this.tile_texture_coords = [];
        this.sprite_vertex_coords = [];
        this.sprite_texture_coords = [];
    }
    
    glixl.Scene.prototype.initialise_viewport = function(parameters)
    {
        this.viewport.x = parameters.x || 0;
        this.viewport.y = parameters.y || 0;
        
        this.viewport.width = parameters.width || this.width;
        this.viewport.height = parameters.height || this.height;
        
        this.viewport_matrix = [
            1,  0, 0, 0,
            0,  1, 0, 0,
            -this.viewport.x, -this.viewport.y, 1, 0,
            0,  0, 0, 1
        ];
        
        this.projection_matrix = [
            2 / this.viewport.width, 0, 0, 0,
            0, -2 / this.viewport.height, 0, 0,
            0, 0, -2 / this.height, 0,
            -1, 1, 0.999999, 1,
        ];
    }
    
    glixl.Scene.prototype.set_viewport = function(x, y)
    {
        this.viewport.x = x;
        this.viewport.y = y;
        
        this.viewport_matrix = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            -this.viewport.x, -this.viewport.y, 1, 1,
            
        ];
    }
    
    glixl.Scene.prototype.add_sprite = function(sprite)
    {
        this.sprites.push(sprite);
    }
    
    glixl.Scene.prototype.add_tile = function(tile)
    {
        var col = Math.floor(tile.x / tile.width);
        var row = Math.floor(tile.y / tile.height);
        
        this.tiles.push(tile);
        
        /*if (this.tiles[this.columns*row+col])
        {
            this.tiles[this.columns*row+col].push(tile);
        }
        else
        {
            this.tiles[this.columns*row+col] = tile; //[tile];
        }*/
    }
    
    glixl.Scene.prototype.update = function()
    {
        var vertices = [];
        var tex_coords = [];
        
        var x1, x2, y1, y2, z;
        for(var i=0 ; i<this.tiles.length ; i++)
        {
            x1 = this.tiles[i].x;
            y1 = this.tiles[i].y - this.tiles[i].z;
            x2 = this.tiles[i].x + this.tiles[i].width;
            y2 = this.tiles[i].y + this.tiles[i].height - this.tiles[i].z;
            z = this.tiles[i].y;
            
            vertices.push( x1,     y1,     z,
                           x2,     y1,     z,
                           x1,     y2,     z,
                           x1,     y2,     z,
                           x2,     y1,     z,
                           x2,     y2,     z );
                           
            tex_coords.push.apply( tex_coords, this.sprite_sheet.get_texture_coordinates(this.tiles[i].frame) );
        }
        
        this.context.bindBuffer(this.context.ARRAY_BUFFER, this.tile_vertex_buffer);
        this.context.bufferData(this.context.ARRAY_BUFFER, new Float32Array(vertices), this.context.STREAM_DRAW);
        
        this.context.bindBuffer(this.context.ARRAY_BUFFER, this.tile_texture_buffer);
        this.context.bufferData(this.context.ARRAY_BUFFER, new Float32Array(tex_coords), this.context.STREAM_DRAW);
        
        var vertices = [];
        var tex_coords = [];
        
        var x1, x2, y1, y2, z;
        for(var s=0 ; s<this.sprites.length ; s++)
        {
            this.sprites[s].update();
            
            x1 = this.sprites[s].x;
            y1 = this.sprites[s].y - this.sprites[s].z;
            x2 = this.sprites[s].x + this.sprites[s].width;
            y2 = this.sprites[s].y + this.sprites[s].height - this.sprites[s].z;
            z = this.sprites[s].y;
            
            vertices.push( x1,     y1,     z,
                           x2,     y1,     z,
                           x1,     y2,     z,
                           x1,     y2,     z,
                           x2,     y1,     z,
                           x2,     y2,     z );
                           
            tex_coords.push.apply( tex_coords, this.sprite_sheet.get_texture_coordinates(this.sprites[s].frame) );
        }
        
        this.context.bindBuffer(this.context.ARRAY_BUFFER, this.sprite_vertex_buffer);
        this.context.bufferData(this.context.ARRAY_BUFFER, new Float32Array(vertices), this.context.STREAM_DRAW);
        
        this.context.bindBuffer(this.context.ARRAY_BUFFER, this.sprite_texture_buffer);
        this.context.bufferData(this.context.ARRAY_BUFFER, new Float32Array(tex_coords), this.context.STREAM_DRAW);
        
        //this.set_viewport(30, 300);
    }
    
    glixl.Scene.prototype.draw = function()
    {
        this.context.uniformMatrix4fv(this.viewport_uniform, false, this.viewport_matrix);
        this.context.uniformMatrix4fv(this.projection_uniform, false, this.projection_matrix);
        
        
        this.context.bindBuffer(this.context.ARRAY_BUFFER, this.sprite_vertex_buffer);
        this.context.vertexAttribPointer(this.position_attribute, 3, this.context.FLOAT, false, 0, 0);
        
        this.context.bindBuffer(this.context.ARRAY_BUFFER, this.sprite_texture_buffer);
        this.context.vertexAttribPointer(this.texture_attribute, 2, this.context.FLOAT, false, 0, 0);
        
        this.context.drawArrays(this.context.TRIANGLES, 0, this.sprites.length * 6);
        
        
        this.context.bindBuffer(this.context.ARRAY_BUFFER, this.tile_vertex_buffer);
        this.context.vertexAttribPointer(this.position_attribute, 3, this.context.FLOAT, false, 0, 0);
        
        this.context.bindBuffer(this.context.ARRAY_BUFFER, this.tile_texture_buffer);
        this.context.vertexAttribPointer(this.texture_attribute, 2, this.context.FLOAT, false, 0, 0);
        
        this.context.drawArrays(this.context.TRIANGLES, 0, this.tiles.length * 6);
    }
    
    return glixl;
    
})(glixl || {});