function RPG()
{		
	var MAP_SIZE = [20, 18, 3] // cols x rows x depth
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
				
		protag = new glixl.Sprite( {sprite_sheet: sprite_sheet, x: 32*2*1, y: 32*2*7, z:1, size:[16, 16], scale: SCALE, frame:41} );		
		glixl.scene.add_sprite(protag);
        
        spr = new glixl.Sprite( {sprite_sheet: sprite_sheet, x: 32*18, y: 32*16, z:1, size:[16, 16], scale: SCALE, frame:42} );		
		glixl.scene.add_sprite(spr);
		
		protag.vx = 0;
		protag.vy = 0;
		protag.speed = 160; //pixels per second
		protag.move_timer = (new Date()).getTime();
		
		protag.move = function()
		{
			var now = (new Date()).getTime();
			var delta = now - this.move_timer;
			
			var last_x = this.x;
			var last_y = this.y;
			
			this.x += Math.round(this.vx * (delta / 1000 * this.speed));	
			this.vx = 0;
			
			this.y += Math.round(this.vy * (delta / 1000 * this.speed));
			this.vy = 0;
			
			if (glixl.scene.collide(this))
			{
				this.x = last_x;
				this.y = last_y;
			}
				
			this.move_timer = now;
			glixl.scene.center_on(this);
			this.redraw = true;
		}
	}
	
	this.update = function()
	{
		if (glixl.key_pressed("d"))// || quint.touched("right"))
		{
			//protag.set_animation(protag.animations.right);
			protag.vx = 1;
		}
		if (glixl.key_pressed("s"))// || quint.touched("down"))
		{
			//protag.set_animation(protag.animations.down);
			protag.vy = 1
		}
		
		if (glixl.key_pressed("a"))// || quint.touched("left"))
		{
			//protag.set_animation(protag.animations.left);
			protag.vx = -1;
		}
		if (glixl.key_pressed("w"))// || quint.touched("up"))
		{
			//protag.set_animation(protag.animations.up);
			protag.vy = -1
		}
		
		protag.move();
        spr.redraw = true;
		document.getElementById('fps').innerHTML = glixl.fps;
		
		if (glixl.mouse_down && click_timer < 0)
        {
            var path = tilemap.find_path([protag.x, protag.y], [glixl.mouse_x, glixl.mouse_y], protag.z, true);
            console.log(path);
            click_timer = 20;
		    //console.log(glixl.mouse_x, glixl.mouse_y);
        }
        click_timer -= 1;
	}
}