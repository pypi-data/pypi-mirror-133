pyGL is an Python Graphical Librairy for **python**
You can do anything you want with it 

**DOCUMENTATION**
-
- Import the lib
- After do this method : 
> app = Window("App name", width, height)
- Do a *while* loop
- After use the method 
>app.clearScreen()
- You can set your max FPS by doing 
>app.setMaxFPS(maxFPS)
- You can add a background color, you need todo 
>app.setBackgroundColor(color)
- At the end you need todo an app.loop()

**DRAWING/Position**
-
- In this Engine you have Vector2 and Transform; contains two **Vector2** Object, One is Position and the other is Scale
- Drawing a basic line is Simple :
> app.DrawLine(pos1 : Vector2, pos 2 : Vector2, color, linewidth, outline)
- Drawing a you have two methods; fast and slow
- SLOW :
> app.drawRect(Transform, color)
- FAST :
> app.fdr(x,y,w,h,c)

**MOVING A TRANSFORM/SCALING**
-
- you can use Transfom for Moving and Scaling or just Moving by a presise axis
- Moving
> transform.Translate(movX,movY)
> 
> //Recommended : do an transform.Update()
- Scaling
> transform.Scale(scaleX,scaleY)
> 
> //Recommended : do an transform.Update()
- Fixed Movement / Scaling
> transform.x or y = VALUE **OR** tranform.position.x or y = VAULE
> 
> transform.w or h = VALUE **OR** transform.scale.x or y = VALUE

# Constant usefull
Object -> an array stock all of the transform of the objects (width, height, x, y)

#Drawing Images
- To print images you need to get them / load
- Loading
> Image = app.LoadImage(Path)
- Print the Image
> app.DisplayImage(Image, x, y)