var Wiz = function(parameters)
{
    glixl.Sprite.call(this, parameters);
}

Wiz.prototype.update = function()
{
    glixl.Sprite.prototype.update.call(this);
    
    //this.x += 3;
    if (this.x > my_game.scene.width)
        this.x = 0;
    
    //this.y += 3;
    if (this.y > my_game.scene.height)
        this.y = 0;
    
    my_game.scene.center_on(this);
}
extend(glixl.Sprite, Wiz);


var RPG = function()
{	
    glixl.Game.call(this, {});
    
    var sprite_sheet = new glixl.SpriteSheet({context: this.context, src: 'tiles.png', frame_size: [16, 16]});
    
    var scene = new glixl.Scene({ context: this.context, width: this.width*2, height: this.height*2, sprite_sheet: sprite_sheet, tile_size: {width: 32, height: 32} });
    
    var wiz = new Wiz({frame: 41, x: 320, y:105, z:32, width:32, height:32});
    wiz.add_animation('walk_down', [50, 51, 52, 53], 120);
    wiz.set_animation('walk_down');
    scene.add_sprite(wiz);
    var wiz = new glixl.Sprite({frame: 50, x: 80, y:266, z:16, width:32, height:32});
    wiz.add_animation('walk_down', [50, 51, 52, 53], 120);
    wiz.set_animation('walk_down');
    scene.add_sprite(wiz);
    
    var MAP_SIZE = [44, 32];
    
    for (var r=0 ; r<MAP_SIZE[1] ; r++)
		{
            for (var c=0 ; c<MAP_SIZE[0] ; c++)
			{
                if (typeof map[r*MAP_SIZE[0]+c] == 'object')
                {
                    for (var t=0 ; t<map[r*MAP_SIZE[0]+c].length ; t++)
                    {
                        scene.add_tile(new glixl.Tile({ frame:map[r*MAP_SIZE[0]+c][t], x:c*32 , y:r*32, z:t*32, width:32, height: 32 }));
                    }
                }
                else
                {
                    scene.add_tile(new glixl.Tile({ frame:map[r*MAP_SIZE[0]+c], x:c*32 , y:r*32, z:0, width:32, height: 32 }));
                    
                    
                }
			}
		}
    
    /*for (var i=0 ; i<10 ; i++)
    {
        wiz = new glixl.Sprite({frame: 41, x: 120, y:i*32+16, z:32, width:32, height:32});
        scene.add_sprite(wiz);
    }*/
    
    this.set_scene(scene);
}

RPG.prototype.update = function()
{
    document.getElementById('fps').innerHTML = this.fps;
}

extend(glixl.Game, RPG);