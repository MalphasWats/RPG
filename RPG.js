function RPG()
{		
	var MAP_SIZE = [20, 18, 3] // cols * rows * depth
	var SCALE = 2;
			
	var protag, spr;
	
	var sprite_sheet;
	var tilemap;
	
	var global_timer = (new Date()).getTime();
	var tick_length = 1500
    
    var click_timer = 0;
	
	this.init = function()
	{
		sprite_sheet = new glixl.SpriteSheet({src:'tiles.png', frame_size:[16, 16]})
		
        tilemap = new glixl.TileMap({sprite_sheet: sprite_sheet, dimensions: MAP_SIZE, scale:SCALE});
        for (var r=0 ; r<MAP_SIZE[1] ; r++)
		{
            for (var c=0 ; c<MAP_SIZE[0] ; c++)
			{
                if (typeof map[r*MAP_SIZE[0]+c] == 'object')
                {
                    for (var t=0 ; t<map[r*MAP_SIZE[0]+c].length ; t++)
                    {
                        tilemap.push_tile(c, r, new glixl.Tile({frame:map[r*MAP_SIZE[0]+c][t], collidable: map[r*MAP_SIZE[0]+c][t] == 9}));
                    }
                }
                else
                {
                    tilemap.push_tile(c, r, new glixl.Tile({frame:map[r*MAP_SIZE[0]+c], collidable: map[r*MAP_SIZE[0]+c] == 9}));
                    
                    
                }
			}
		}
		glixl.scene.set_active_tilemap(tilemap);
				
		protag = new glixl.Sprite( {sprite_sheet: sprite_sheet, x: 32*SCALE*1, y: 32*SCALE*7, z:1, size:[16, 16], scale: SCALE, frame:41} );		
		glixl.scene.add_sprite(protag);
        
        spr = new glixl.Sprite( {sprite_sheet: sprite_sheet, x: 32*18, y: 32*16, z:1, size:[16, 16], scale: SCALE, frame:42} );		
		glixl.scene.add_sprite(spr);
		
		protag.vx = 0;
		protag.vy = 0;
		protag.speed = 140; //pixels per second
		protag.move_timer = (new Date()).getTime();
		
		protag.destination = false;
		protag.path = []
		
		protag.move = function()
		{
			var now = (new Date()).getTime();
			var delta = now - this.move_timer;
			
			var dx = Math.abs(this.x - this.destination.x);
			var next_step = Math.round(this.vx * (delta / 1000 * this.speed));
			if (dx < next_step)
			    next_step = dx*this.vx;
			    
			this.x += next_step;
			
			var dy = Math.abs(this.y - this.destination.y);
			var next_step = Math.round(this.vy * (delta / 1000 * this.speed));
			if (dy < next_step)
			    next_step = dy*this.vy;
			
			this.y += next_step;
				
			this.move_timer = now;
			glixl.scene.center_on(this);
			this.redraw = true;
		}
		
		protag.set_path = function(path)
		{
    		this.path = path;
    		this.destination = this.path.shift();
    		this.destination.x += (this.width/2) * this.scale;
            this.destination.y += (this.height/4) * this.scale;
		} 
		
		protag.move_ = function()
		{
    		if (this.destination)
            {
                if (this.x == this.destination.x && this.y == this.destination.y)
                {
                    if (this.path.length > 0)
                    {
                        this.destination = this.path.shift()
                        this.destination.x += (this.width/2) * this.scale;
                        this.destination.y += (this.height/4) * this.scale;
                    }
                    else
                    {
                        this.destination = false
                    }
                }
                this.vx = 0
                this.vy = 0
                if(this.x > this.destination.x)
                {
                    this.vx = -1;
                }
                else if (this.x < this.destination.x)
                {
                    this.vx = 1;
                }
                if(this.y > this.destination.y)
                {
                    this.vy = -1;
                }
                else if (this.y < this.destination.y)
                {
                    this.vy = 1;
                }
                
            }
    		this.move()
		}
		
	}
	
	this.update = function()
	{
        spr.redraw = true;
		
		if (glixl.mouse_down && click_timer < 0)
        {
            var path = tilemap.find_path([protag.x, protag.y], [glixl.mouse_x, glixl.mouse_y], protag.z, true);
            protag.set_path(path);

            click_timer = 20;
        }
        click_timer -= 1;
        
        protag.move_();
        
        document.getElementById('fps').innerHTML = glixl.fps;
	}
}