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
        
        this.tilemap = new Array(this.columns);
        for (var c=0 ; c<this.columns ; c++)
        {
            this.tilemap[c] = new Array(this.rows);
            for (var r=0 ; r<this.rows ; r++)
            {
                this.tilemap[c][r] = new Array(this.rows);
                for (var d=0 ; d<this.rows ; d++)
                {
                    this.tilemap[c][r][d] = false;
                }
            }
        }
        
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
    
    /*glixl.Scene.prototype.set_viewport = function(x, y)
    {
        this.viewport.x = x;
        this.viewport.y = y;
        
        this.viewport_matrix = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            -this.viewport.x, -this.viewport.y, 1, 1,
            
        ];
    }*/
    
    glixl.Scene.prototype.add_sprite = function(sprite)
    {
        this.sprites.push(sprite);
    }
    
    glixl.Scene.prototype.add_tile = function(tile)
    {
        var col = Math.floor(tile.x / tile.width);
        var row = Math.floor(tile.y / tile.height);
        var depth = Math.floor(tile.z / tile.height);
        
        this.tiles.push(tile);
        
        this.tilemap[col][row][depth] = tile;
        
        /*if (this.tilemap[row])
        {
            if (this.tilemap[row][col])
            {
                this.tilemap[row][col].push(tile);
            }
            else
            {
                this.tilemap[row][col] = [tile];
            }
        }
        else
        {
            this.tilemap[row] = [];
            this.tilemap[row][col] = [tile];
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
    
    glixl.Scene.prototype.center_on = function(object)
    {
        if (object.x && object.y)
        {
            var prev_x = this.viewport.x;
            var prev_y = this.viewport.y;
            this.viewport.x = Math.floor(object.x - this.viewport.width / 2);
            this.viewport.y = Math.floor(object.y - this.viewport.height / 2);
        }
        if (this.viewport.x < 0)
            this.viewport.x = 0;
        if (this.viewport.y < 0)
            this.viewport.y = 0;
        if (this.viewport.x  > this.width - this.viewport.width)
            this.viewport.x = this.width - this.viewport.width;
        if (this.viewport.y > this.height - this.viewport.height)
            this.viewport.y = this.height - this.viewport.height;
        
        this.viewport_matrix = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            -this.viewport.x, -this.viewport.y, 1, 1,
            
        ];
    }
    
    glixl.Scene.prototype.find_path = function(start, end)
    {
        var start_col = parseInt(start_position[0] / (this.tile_width * this.scale));
        var start_row = parseInt(start_position[1] / (this.tile_height * this.scale));
  
        var end_col = parseInt(end_position[0] / (this.tile_width * this.scale));
        var end_row = parseInt(end_position[1] / (this.tile_height * this.scale));
  
        if (start_col === end_col && start_row === end_row)
            return [{x: start_position[0], y:start_position[1]}];
  
        var col = start_col;
        var row = start_row;
        var step = 0;
        var score = 0;
        //travel corner-to-corner, through every square, plus one, just to make sure
        var max_distance = (this.columns*this.rows * 2)+1;
  
        var open_nodes = new Array(this.columns);
        for(var i=0 ; i < this.columns ; i++) 
        {
            open_nodes[i] = new Array(this.rows);
            for(var j=0 ; j < this.rows ; j++) 
            {
                open_nodes[i][j] = false;
            }
        }
        open_nodes[col][row] = {parent: [], G: 0, score: max_distance};
  
        var closed_nodes = new Array(this.columns);
        for(var i=0 ; i < this.columns ; i++) 
        {
            closed_nodes[i] = new Array(this.rows);
            for(var j=0 ; j < this.rows ; j++) 
            {
                closed_nodes[i][j] = false;
            }
        }

        var crowFlies = function(from_node, to_node) 
        {
            return Math.abs(to_node[0]-from_node[0]) + Math.abs(to_node[1]-from_node[1]);
        };
  
        var findInClosed = function(col, row) 
        {
            if (closed_nodes[col][row])
                return true;
            else 
                return false;
        }
  
        while ( !(col === end_col && row === end_row) ) 
        {
            /**
             *  add the nodes above, below, to the left and right of the current node
             *  if it doesn't have a sprite in it, and it hasn't already been added
             *  to the closed list, recalculate its score from the current node and
             *  update it if it's already in the open list.
             */
            var left_right_up_down = [];
            if (col > 0) 
            { 
                left_right_up_down.push([col-1, row]);
                if (row > 0)
                {
                    left_right_up_down.push([col-1, row-1]);
                }
            }
            if (col < this.columns-1)
            { 
                left_right_up_down.push([col+1, row]);
                if (row < this.rows-1)
                {
                    left_right_up_down.push([col+1, row+1]);
                }
            }
            if (row > 0)
            {
                left_right_up_down.push([col, row-1]);
                if (col < this.columns-1)
                {
                    left_right_up_down.push([col+1, row-1]);
                }
            }
            if (row < this.rows-1) 
            {
                left_right_up_down.push([col, row+1]);
                if (col > 0)
                {
                    left_right_up_down.push([col-1, row+1]);
                }
            }
        
            for (var i=0 ; i<left_right_up_down.length ; i++) 
            {
                var c = left_right_up_down[i][0];
                var r = left_right_up_down[i][1];
                if ( (typeof this.tilemap[r][c] == 'undefined' || typeof this.map[r][c][depth] == 'undefined' || !this.map[r*this.columns+c][depth].collidable) && !findInClosed(c, r) )
                {
                    score = step+1+crowFlies([c, r] , [end_col, end_row]);
                    if (!open_nodes[c][r] || (open_nodes[c][r] && open_nodes[c][r].score > score)) 
                    {
                        open_nodes[c][r] = {parent: [col, row], G: step+1, score: score};
                    }
                }
            }
        
            /**
             *  find the lowest scoring open node
             */
            var best_node = {node: [], parent: [], score: max_distance, G: 0};
            for (var i=0 ; i<this.columns ; i++) 
            {
                for(var j=0 ; j<this.rows ; j++) 
                {
                    if (open_nodes[i][j] && open_nodes[i][j].score < best_node.score) 
                    {
                        best_node.node = [i, j];
                        best_node.parent = open_nodes[i][j].parent;
                        best_node.score = open_nodes[i][j].score;
                        best_node.G = open_nodes[i][j].G;
                    }
                }
            }
            
            if (best_node.node.length === 0) //open_nodes is empty, no route found to end node
                return [];
        
            //This doesn't stop the node being added again, but it doesn't seem to matter
            open_nodes[best_node.node[0]][best_node.node[1]] = false;
        
            col = best_node.node[0];
            row = best_node.node[1];
            step = best_node.G;
        
            closed_nodes[col][row] = {parent: best_node.parent};
        }
  
        /**
         *  a path has been found, construct it by working backwards from the
         *  end node, using the closed list
         */
        var path = [];
        var current_node = closed_nodes[col][row];
        path.unshift({x: col*this.tile_width*this.scale, y: row*this.tile_height * this.scale});
        while(! (col === start_col && row === start_row) )
        {
            col = current_node.parent[0];
            row = current_node.parent[1];
            path.unshift({x: col*this.tile_width*this.scale, y: row*this.tile_height * this.scale});
            current_node = closed_nodes[col][row];
        }
        
        return path;
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