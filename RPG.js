function RPG()
{		
	var MAP_SIZE = [20, 18, 3] // cols * rows * depth
	var SCALE = 2;
			
	var player, spr;
	
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
                        tilemap.push_tile(c, r, new glixl.Tile({frame:map[r*MAP_SIZE[0]+c][t], collidable: SOLID_TILES.indexOf(map[r*MAP_SIZE[0]+c][t]) > -1}));
                    }
                }
                else
                {
                    tilemap.push_tile(c, r, new glixl.Tile({frame:map[r*MAP_SIZE[0]+c], collidable: SOLID_TILES.indexOf(map[r*MAP_SIZE[0]+c][t]) > -1}));
                    
                    
                }
			}
		}
		glixl.scene.set_active_tilemap(tilemap);
		
		player = new Player({sprite_sheet: sprite_sheet, x: 32*SCALE*1, y: 32*SCALE*7, z:1, size:[16, 16], scale: SCALE, frame:41, speed: 140});		
		glixl.scene.add_sprite(player);
        
        spr = new Mob( {sprite_sheet: sprite_sheet, x: 32*18, y: 32*16, z:1, size:[16, 16], scale: SCALE, frame:42, speed: 80, home: [32*18, 32*16]} );		
		glixl.scene.add_sprite(spr);		
	}
	
	this.update = function()
	{
        //spr.redraw = true;
		var path;
		if (glixl.mouse_down && click_timer < 0)
        {
            path = tilemap.find_path([player.x, player.y], [glixl.mouse_x, glixl.mouse_y], player.z);
            path.shift();
            player.set_path(path);

            click_timer = 20;
            spr.clear_path();
        }
        click_timer -= 1;
        
        if (Math.abs( (spr.x-player.x) + (spr.y-player.y) ) < 150 && Math.abs( (spr.x-spr.home[0]) + (spr.y-spr.home[1]) ) < 300)
        {
            path = tilemap.find_path([spr.x, spr.y], [player.x, player.y], spr.z);
            path.shift();
            spr.set_path(path);
        }
        else
        {
            path = tilemap.find_path([spr.x, spr.y], spr.home, spr.z); 
            path.shift();
            spr.set_path(path);
        }
        
        player.update();
        spr.update();
        glixl.scene.center_on(player);
        
        document.getElementById('fps').innerHTML = glixl.fps;
	}
}