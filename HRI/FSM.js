// Define states
const STATES = {
    IDLE: 'IDLE',
    FIRST: 'FIRST',
    SECOND: 'SECOND',
    THIRD: 'THIRD',
    FOURTH: 'FOURTH',
    FIFTH: 'FIFTH',
    TERMINAL: 'TERMINAL',
      
  };
  
  let currentState = STATES.IDLE;
  
  
  const STATE_COLORS = {
    IDLE: { r: 0, g: 0, b: 255 },//blue
    FIRST: { r: 255, g: 0, b: 0 },//red
    SECOND: { r: 0, g: 255, b: 0 },//green
    THIRD: { r: 255, g: 252, b: 9 },//yellow
    FOURTH: { r: 128, g: 0, b: 128 },//purple
    FIFTH: { r: 252, g: 105, b: 180 },//pink
    TERMINAL: { r: 255, g: 140, b: 0 },//orange
  };
  
  async function stateIdle(){
      await scrollMatrixText('Hello', {r:0, g:0, b:255}, 15, true);
      await speak("Reached State " + currentState);
      await spin(360,3);
      await delay(3);
  }
  
  async function stateOne(){
      await speak("Reached State" + currentState);
      await scrollMatrixText('State 1', {r:255, g:0, b:0}, 15, true);
      await spin(360,3);
      await delay(3);
  }
  
  async function stateTwo(){
      await speak("Reached State" + currentState);
      await scrollMatrixText('State 2', {r:0, g:252, b:0}, 15, true);
      await spin(360,3);
      await delay(3);
  }
  
  async function stateThree(){
      await speak("Reached State" + currentState);
      await scrollMatrixText('State 3', {r:255, g:252, b:9}, 15, true);
      await spin(360,3);
      await delay(3);
  }
  
  async function stateFour(){
      await speak("Reached State" + currentState);
      await scrollMatrixText('State 4', {r: 128, g: 0, b: 128 }, 15, true);
      await spin(360,3);
      await delay(3);
  }
  
  async function stateFive(){
      await speak("Reached State" + currentState);
      await scrollMatrixText('State 5', { r: 255, g: 105, b: 180 }, 15, true);
      await spin(360,3);
      await delay(3);
  }
  
  async function stateTerminal(){
      await speak("Reached State" + currentState);
      await scrollMatrixText('Terminal State', {r: 255, g: 140, b: 0 }, 15, true);
      await exitProgram();
  }
  
  
  async function changeState(newState) {
    currentState = newState;
    let color = STATE_COLORS[newState];
    await setMainLed(color);
  }
  
  
  async function onCollision() {
      await speak("Collision Detected");
      
      switch (currentState) {
        case STATES.IDLE:
            await changeState(STATES.FIRST);
            break;
              
        case STATES.FIRST:
            await changeState(STATES.SECOND);
            break;
              
        case STATES.SECOND:
            await changeState(STATES.THIRD);
            break;
              
        case STATES.THIRD:
            await changeState(STATES.FOURTH);
            break;
              
        case STATES.FOURTH:
            await changeState(STATES.FIFTH);
          break;
              
        case STATES.FIFTH:
            await changeState(STATES.TERMINAL);
            break;
              
        case STATES.TERMINAL:
          break;
              
      return; 
      }
  }
  
  async function fsmLoop() {
    while (true) {
      switch (currentState) {
      case STATES.IDLE:
          await stateIdle();
          break;
              
        case STATES.FIRST:
          await stateOne();
          break;
        
        case STATES.SECOND:
          await stateTwo();
          break;
  
        case STATES.THIRD:
          await stateThree();
          break;
              
        case STATES.FOURTH:
          await stateFour();
          break;
              
        case STATES.FIFTH:
          await stateFive();
          break;
              
        case STATES.TERMINAL:
          await stateTerminal();
          break;
      }
    }
  }
  
  registerEvent(EventType.onCollision, onCollision);
  
  async function startProgram() {
    await fsmLoop();
  }
  
  