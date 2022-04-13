// Deal w websockets stuff :)
let viewer_positions = [{x:0, y:0}];
function setup_socket(){
    // Create WebSocket connection.
  const socket = new WebSocket('ws://localhost:8001', 'echo-protocol');
  // Connection opened
  socket.addEventListener('open', function () {
      console.log("Opened websocket connection");
  });
  
  // Listen for messages
  socket.addEventListener('message', function (event) {
    // expect json of form {positions:[{x: <float>, y: <float>}, ...]}
    // where x and y 0<=x<=100
    try{
      viewer_positions = JSON.parse(event.data).positions;
      console.log('Message from server: ', viewer_positions);
    } catch(err){
      console.log("Parsing socket data failed with error:");
      console.error(err);
    }
  });
}

const size = {x: 1400, y:800}
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

// Deal with video
function setup_video(){
  let vid = createVideo("http://localhost:8000/test.MP4", (a)=>console.log(a))
  vid.loop();
  setTimeout(()=>{vid.remove()}, 700)
}

function setup() {
  setup_sound();
  setup_socket();
  for( let i = 0; i < p_side; i++){
    let row = [];
    let original_row = [];
    for( let j = 0; j < p_side; j++){
      row.push({x: i * (size.x/p_side) + (size.x/p_side/2), y:j * (size.y/p_side) + (size.y/p_side/2), acc: {x: 0, y:0}});
      original_row.push({x: i * (size.x/p_side) + (size.x/p_side/2), y:j * (size.y/p_side) + (size.y/p_side/2), acc: {x: 0, y:0}});
    } 
    points.push(row);
    original_points.push(original_row);
  }
  createCanvas(size.x, size.y);
  noStroke();
}

function distance(x1, y1, x2, y2){
  return sqrt((x1 - x2)**2 + (y1-y2)**2);
}

function draw() {
  if(int(random(0, 600)) == 0){
    setup_video();
  }
  // background(255);
  fill(200);

  // Get positions from websockets data.
  const v_pos = {x: 0, y:0};
  v_pos.x = (viewer_positions[0].x * size.x) / 100;
  v_pos.y = (viewer_positions[0].y * size.y) / 100;
  // circle(v_pos.x, v_pos.y, 50);

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
      if (v_pos.x > screen_margin && v_pos.x < size.x-screen_margin && v_pos.y > screen_margin && v_pos.y < size.y-screen_margin){
        // distance from mouse:
        let d = distance(p.x, p.y, v_pos.x, v_pos.y);
        p.acc.x += dir.x + (v_pos.x - p.x) / (1*(d**1.2));
        p.acc.y += dir.y + (v_pos.y - p.y) / (1*(d**1.2));
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
      // let s_obj = os[i][j];
      // if(p.acc.x + p.acc.y > 1.5){
      //   if(s_obj.on == false){
      //     s_obj.on = true;
      //     s_obj.osc.start();
      //   }
      // } else {
      //   s_obj.on = false;
      //   s_obj.osc.stop();
      // }
      fill(255-p.acc.x*100, 255-p.acc.y * 100, 255-sin(p.acc.y) * 100)
      circle(p.x, p.y, 8);
    } 
  }
}