# yb2gpx 

converts data obtained from YB Tracking Race Viewer to GPX format

## How to get the YB data
Answer I don't know any official way. 

### This is how I got it:

Get Race meta data:  
```bash
curl https://yb.tl/JSON/corw2019/RaceSetup --output ~/tmp/spin-cup/RaceSetup.json
```

Get the tracks 
```bash 
curl https://yb.tl/BIN/corw2019/AllPositions3 --output ~/tmp/spin-cup/AllPositions3.bin
```

Indeed I didn't care to reverse engineer the content of AllPositions3.bin, instead just put a breakpoint at this line  

```js
viewer.initialiseLeaderboard()
```

of the function
```js
Race.prototype.getAllPositions = function() 
```

Then copied the content of local variable i to the clipboard and then to the file allpositions.json


## To create GPX file run
 
```bash
python yb2gpx.py --positions=~/tmp/spin-cup/allpositions.json --setup=~/tmp/spin-cup/race-setup.json --gpx=~/tmp/spin-cup/spin2019-yb-tracks.gpx
```
