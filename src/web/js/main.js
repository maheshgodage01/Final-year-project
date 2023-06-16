
//user clicked button
document.getElementById("userInputButton").addEventListener("click", getUserInput);
//user pressed enter '13'
document.getElementById("userInput").addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        //cancel the default action
        event.preventDefault();
        //process event
        getUserInput();
    }
});

document.getElementById("gesture-recognition").addEventListener("click", gesture_rec);
document.getElementById("voice_assistant").addEventListener("click", voice_ast);
document.getElementById("exit").addEventListener("click", exit);



eel.expose(addUserMsg);
eel.expose(addAppMsg);
// eel.expose(respond);


function addUserMsg(msg) {
    element = document.getElementById("messages");
    element.innerHTML += '<div class="message from ready rtol">' + msg + '</div>';
    element.scrollTop = element.scrollHeight - element.clientHeight - 15;
    //add delay for animation to complete and then modify class to => "message from"
    index = element.childElementCount - 1;
    setTimeout(changeClass.bind(null, element, index, "message from"), 500);
}

function addAppMsg(msg) {
    element = document.getElementById("messages");
    element.innerHTML += '<div class="message to ready ltor">' + msg + '</div>';
    element.scrollTop = element.scrollHeight - element.clientHeight - 15;
    //add delay for animation to complete and then modify class to => "message to"
    index = element.childElementCount - 1;
    setTimeout(changeClass.bind(null, element, index, "message to"), 500);
}

function changeClass(element, index, newClass) {
    console.log(newClass +' '+ index);
    element.children[index].className = newClass;
}


function getUserInput() {
    element = document.getElementById("userInput");
    msg = element.value;
    if (msg.length != 0) {
        element.value = "";
        eel.getUserInput(msg);
        // addUserMsg(msg+"from js");
    }
}

function gesture_rec(){
    l1 = document.getElementById("gesture-recognition");
    // var start=false;
    if(l1.innerHTML=="Launch Gesture Recognition"){
        eel.getUserInput("launch gesture recognition")
        l1.innerHTML="Stop Gesture Recognition";
    }
    else if(l1.innerHTML=="Stop Gesture Recognition"){
        eel.getUserInput("stop gesture recognition");
        l1.innerHTML="Start Gesture Recognition";
    }

}

function voice_ast(){
    l1 = document.getElementById("voice_assistant");
    // var start=false;
    if(l1.innerHTML=="Start Voice Assistant"){
        eel.getUserInput("start voice assistant")
        l1.innerHTML="Stop Voice Assistant";
    }
    else if(l1.innerHTML=="Stop Voice Assistant"){
        eel.getUserInput("stop voice assistant");
        l1.innerHTML="Start Voice Assistant";
    }
}

function exit(){
    l1 = document.getElementById("exit");
        eel.getUserInput("exit")
}