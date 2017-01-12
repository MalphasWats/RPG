
var RPG = function()
{	
    glixl.Game.call(this, {});
    
    var sprite_sheet = new glixl.SpriteSheet({context: this.context, src: 'tiles.png', frame_size: [16, 16]});
    
    var scene = new glixl.Scene({ context: this.context, width: this.width*2, height: this.height*2, sprite_sheet: sprite_sheet, tile_size: {width: 32, height: 32} });
    
    var wiz = new glixl.Sprite({frame: 41, x: 0, y:250, z:0, width:32, height:32});
    
    scene.add_sprite(wiz);
    var wiz = new glixl.Sprite({frame: 40, x: 8, y:266, z:16, width:32, height:32});
    
    scene.add_sprite(wiz);
    
    //var tile = new glixl.Tile({frame: 0, x: 0, y:0, z:0, width:32, height:32});
    
    //scene.add_tile(tile);
    
    var MAP_SIZE = [20, 18];
    
    /*for (var r=0 ; r<MAP_SIZE[1] ; r++)
		{
            for (var c=0 ; c<MAP_SIZE[0] ; c++)
			{
                if (typeof map[r*MAP_SIZE[0]+c] == 'object')
                {
                    for (var t=0 ; t<map[r*MAP_SIZE[0]+c].length ; t++)
                    {
                        scene.add_tile(c, r, new glixl.Tile({frame:map[r*MAP_SIZE[0]+c][t], collidable: SOLID_TILES.indexOf(map[r*MAP_SIZE[0]+c][t]) > -1}));
                    }
                }
                else
                {
                    scene.add_tile(c, r, new glixl.Tile({frame:map[r*MAP_SIZE[0]+c], collidable: SOLID_TILES.indexOf(map[r*MAP_SIZE[0]+c][t]) > -1}));
                    
                    
                }
			}
		}*/
    
    /*for (var i=0 ; i<10 ; i++)
    {
        wiz = new glixl.Sprite({frame: 41, x: 120, y:i*32+16, z:0, width:32, height:32});
        scene.add_sprite(wiz);
    }*/
    
    this.set_scene(scene);
}

RPG.prototype.update = function()
{
    document.getElementById('fps').innerHTML = this.fps;
}

extend(glixl.Game, RPG);