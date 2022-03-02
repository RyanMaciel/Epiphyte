const size = 800
const p_side = 20
let points = [];
let original_points = []
const jitter = 0.02;

const os = [];
function setup_sound(){
  for( let i = 0; i < p_side; i++){
    let row = []
    for( let j = 0; j < p_side; j++){
        let osc = new p5.Oscillator('sine');
        osc.freq(800 + random(-200, 200), 0);
        osc.amp(1);
        row.push({osc: osc, on: false});
    }
    os.push(row);
  }
}

function setup() {
  setup_sound();
  for( let i = 0; i < p_side; i++){
    let row = [];
    let original_row = [];
    for( let j = 0; j < p_side; j++){
      row.push({x: i * (size/p_side) + (size/p_side/2), y:j * (size/p_side) + (size/p_side/2), acc: {x: 0, y:0}});
      original_row.push({x: i * (size/p_side) + (size/p_side/2), y:j * (size/p_side) + (size/p_side/2), acc: {x: 0, y:0}});
    } 
    points.push(row);
    original_points.push(original_row);
  }
  createCanvas(size, size);
  noStroke();
}

function distance(x1, y1, x2, y2){
  return sqrt((x1 - x2)**2 + (y1-y2)**2);
}

function draw() {
  let max_dist = sqrt(size**2 + size**2)

  background(255);
  fill(200);
   for( let i = 0; i < points.length; i++){
    for( let j = 0; j < points[0].length; j++){
      
      const p = points[i][j];
      const op = original_points[i][j];
      let dir = {x: 0, y:0};
      if(p.x != op.x && p.y != op.y){
        const o_dist = 100;//distance(p.x, p.y, op.x, op.y)*100;
        dir = {x: (op.x - p.x)/o_dist, y: (op.y- p.y)/o_dist};
      }
      
      // only consider mouse if its on the screen
      const screen_margin = 20;
      if (mouseX > screen_margin && mouseX < size-screen_margin && mouseY > screen_margin && mouseY < size-screen_margin){
        // distance from mouse:
        let d = distance(p.x, p.y, mouseX, mouseY);
        p.acc.x += dir.x + (mouseX - p.x) / (1*(d**1.2));
        p.acc.y += dir.y + (mouseY - p.y) / (1*(d**1.2));
      } else {
        p.acc.x += dir.x;
        p.acc.y += dir.y;
      }
        
      // jitter
      p.acc.x += random(-jitter, jitter);
      p.acc.y += random(-jitter, jitter);
      p.x += p.acc.x;
      p.y += p.acc.y;
      p.acc.x *= 0.99;
      p.acc.y *= 0.99;
      // const acc_con = ((p.acc.x ** 2) + (p.acc.y**2));
      // fill(acc_con * 100, acc_con*99, 100);
      
      // sound
      let s_obj = os[i][j];
      if(p.acc.x + p.acc.y > 1.5){
        if(s_obj.on == false){
          s_obj.on = true;
          s_obj.osc.start();
        }
      } else {
        s_obj.on = false;
        s_obj.osc.stop();
      }
      fill(255-p.acc.x*100, 255-p.acc.y * 100, 255-sin(p.acc.y) * 100)
      circle(p.x, p.y, 8);
    } 
  }
}