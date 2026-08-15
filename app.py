import streamlit as st


# ============================================================
# CONFIG
# ============================================================

WEMOS_IP = "192.168.0.9"


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="SUBMARINE V2",
    page_icon="⚓",
    layout="wide"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #080b10;
        color: white;
    }

    h1 {
        text-align: center;
    }

    h2 {
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.title("⚓ SUBMARINE V2")

st.markdown(
    """
    <h3 style="text-align:center;">
    🟢 PROTOTYPE 2 • DRONE CONTROL
    </h3>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CAMERA
# ============================================================

st.subheader("📹 REAR CAMERA")


camera_html = """
<!DOCTYPE html>

<html>

<head>

<meta
name="viewport"
content="width=device-width, initial-scale=1">

<style>

body {
    margin:0;
    background:#080b10;
    color:white;
    font-family:Arial;
    text-align:center;
}

video {
    width:100%;
    max-width:650px;
    border-radius:15px;
    background:black;
}

button {
    padding:14px 22px;
    margin:10px;
    border:none;
    border-radius:12px;
    font-size:17px;
    font-weight:bold;
}

</style>

</head>

<body>

<video
id="camera"
autoplay
playsinline>
</video>

<br>

<button onclick="startCamera()">
📹 START REAR CAMERA
</button>

<script>

async function startCamera() {

    try {

        const stream =
            await navigator
            .mediaDevices
            .getUserMedia({

                video: {
                    facingMode: {
                        ideal: "environment"
                    }
                },

                audio:false

            });


        document.getElementById(
            "camera"
        ).srcObject = stream;

    }

    catch(error) {

        alert(
            "Camera error: " +
            error.message
        );

    }

}

</script>

</body>

</html>
"""


st.iframe(
    camera_html,
    height=430
)


# ============================================================
# SPEED
# ============================================================

st.subheader("🎚️ MASTER SPEED")


speed = st.slider(
    "Maximum motor speed",
    min_value=0,
    max_value=100,
    value=20,
    step=1
)


st.markdown(
    f"""
    <h2>{speed}%</h2>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DRONE CONTROLLER
# ============================================================

st.subheader("🎮 DRONE-STYLE CONTROL")


controller_html = """
<!DOCTYPE html>

<html>

<head>

<meta
name="viewport"
content="width=device-width, initial-scale=1">

<style>

html,
body {

    margin:0;

    padding:0;

    background:#080b10;

    color:white;

    font-family:Arial;

    touch-action:none;

    user-select:none;

}


/* ==========================================================
   CONTROLLER
   ========================================================== */

#controller {

    width:100%;

    height:520px;

    display:flex;

    justify-content:space-around;

    align-items:center;

    touch-action:none;

}


/* ==========================================================
   STICK AREA
   ========================================================== */

.stickArea {

    width:260px;

    height:330px;

    display:flex;

    justify-content:center;

    align-items:center;

    position:relative;

}


/* ==========================================================
   BASE
   ========================================================== */

.base {

    width:210px;

    height:210px;

    border-radius:50%;

    background:#202833;

    border:5px solid #3b4654;

    position:relative;

    touch-action:none;

}


/* ==========================================================
   STICK
   ========================================================== */

.stick {

    width:78px;

    height:78px;

    border-radius:50%;

    background:#4b83ff;

    position:absolute;

    left:66px;

    top:66px;

    box-shadow:
        0 0 25px
        rgba(75,131,255,0.55);

    pointer-events:none;

}


/* ==========================================================
   LABEL
   ========================================================== */

.label {

    position:absolute;

    bottom:10px;

    width:100%;

    text-align:center;

    color:#aaa;

    font-size:16px;

    font-weight:bold;

}


/* ==========================================================
   DIRECTION LABELS
   ========================================================== */

.direction {

    position:absolute;

    color:#777;

    font-size:20px;

    font-weight:bold;

    pointer-events:none;

}

.up {

    top:10px;

    left:50%;

    transform:translateX(-50%);

}

.down {

    bottom:10px;

    left:50%;

    transform:translateX(-50%);

}

.left {

    left:10px;

    top:50%;

    transform:translateY(-50%);

}

.right {

    right:10px;

    top:50%;

    transform:translateY(-50%);

}


/* ==========================================================
   STATUS
   ========================================================== */

#status {

    position:absolute;

    top:15px;

    left:50%;

    transform:translateX(-50%);

    color:#00ff66;

    font-weight:bold;

}

</style>

</head>


<body>


<div id="status">

🟢 READY

</div>


<div id="controller">


<!-- ========================================================
     LEFT STICK
     THROTTLE
     ======================================================== -->

<div class="stickArea">

    <div
        class="base"
        id="throttleBase"
    >

        <div class="direction up">
            ▲
        </div>

        <div class="direction down">
            ▼
        </div>

        <div
            class="stick"
            id="throttleStick"
        ></div>

    </div>

    <div class="label">
        THROTTLE
    </div>

</div>


<!-- ========================================================
     RIGHT STICK
     STEERING
     ======================================================== -->

<div class="stickArea">

    <div
        class="base"
        id="steeringBase"
    >

        <div class="direction left">
            ◀
        </div>

        <div class="direction right">
            ▶
        </div>

        <div
            class="stick"
            id="steeringStick"
        ></div>

    </div>

    <div class="label">
        STEERING
    </div>

</div>


</div>


<script>


// ============================================================
// CONFIG
// ============================================================

const WEMOS =
    "__WEMOS_IP__";


const SPEED =
    __SPEED__;


// ============================================================
// ELEMENTS
// ============================================================

const throttleBase =
    document.getElementById(
        "throttleBase"
    );


const throttleStick =
    document.getElementById(
        "throttleStick"
    );


const steeringBase =
    document.getElementById(
        "steeringBase"
    );


const steeringStick =
    document.getElementById(
        "steeringStick"
    );


const status =
    document.getElementById(
        "status"
    );


// ============================================================
// VALUES
// ============================================================

let throttle =
    0;


let steering =
    0;


let throttleActive =
    false;


let steeringActive =
    false;


// ============================================================
// STICK GEOMETRY
// ============================================================

const CENTER =
    105;


const MAX =
    65;


// ============================================================
// MOTOR OUTPUT
// ============================================================

function updateMotors() {


    // ========================================================
    // THROTTLE
    // ========================================================

    let baseThrottle =
        throttle;


    // ========================================================
    // STEERING
    //
    // Steering strength depends on the steering stick.
    // ========================================================

    let steer =
        steering;


    // ========================================================
    // MIXING
    //
    // Normal forward steering:
    //
    // throttle + left
    //     left motor slower
    //
    // throttle + right
    //     right motor slower
    //
    // ========================================================

    let left;
    let right;


    if (
        Math.abs(baseThrottle) < 0.03
    ) {

        // ----------------------------------------------------
        // STATIONARY TURN
        //
        // Allow controlled pivoting when throttle is centered.
        // ----------------------------------------------------

        left =
            steer * 0.45;

        right =
            -steer * 0.45;

    }

    else {

        // ----------------------------------------------------
        // MOVING TURN
        // ----------------------------------------------------

        left =
            baseThrottle -
            (
                steer *
                Math.abs(baseThrottle)
            );


        right =
            baseThrottle +
            (
                steer *
                Math.abs(baseThrottle)
            );

    }


    // ========================================================
    // NORMALIZE
    // ========================================================

    const maximum =
        Math.max(
            1,
            Math.abs(left),
            Math.abs(right)
        );


    left =
        left /
        maximum;


    right =
        right /
        maximum;


    // ========================================================
    // SPEED
    // ========================================================

    left =
        left *
        SPEED;


    right =
        right *
        SPEED;


    // ========================================================
    // SEND
    // ========================================================

    sendMotors(
        left,
        right
    );

}


// ============================================================
// SEND TO WEMOS
// ============================================================

let lastSent =
    "";


function sendMotors(
    left,
    right
) {


    const leftValue =
        Math.round(left);


    const rightValue =
        Math.round(right);


    const command =
        leftValue +
        "," +
        rightValue;


    // Avoid duplicate requests

    if (
        command === lastSent
    ) {

        return;

    }


    lastSent =
        command;


    const url =
        "http://" +
        WEMOS +
        "/motors?left=" +
        leftValue +
        "&right=" +
        rightValue;


    fetch(
        url,
        {
            method:"GET",
            cache:"no-store"
        }
    )

    .then(
        function(response) {

            if (
                response.ok
            ) {

                status.innerText =
                    "🟢 L:" +
                    leftValue +
                    "%  R:" +
                    rightValue +
                    "%";

            }

        }
    )

    .catch(
        function(error) {

            status.innerText =
                "🔴 WEMOS CONNECTION ERROR";

            console.log(error);

        }
    );

}


// ============================================================
// STOP
// ============================================================

function stopMotors() {

    throttle = 0;
    steering = 0;


    lastSent = "";


    fetch(
        "http://" +
        WEMOS +
        "/stop",
        {
            method:"GET",
            cache:"no-store"
        }
    )

    .catch(
        function(error) {

            console.log(error);

        }
    );


    status.innerText =
        "🛑 STOPPED";

}


// ============================================================
// RESET STICK
// ============================================================

function resetStick(
    stick
) {

    stick.style.left =
        "66px";

    stick.style.top =
        "66px";

}


// ============================================================
// THROTTLE STICK
// ============================================================

function throttleControl(
    event
) {

    const rect =
        throttleBase
        .getBoundingClientRect();


    let x =
        event.clientX -
        rect.left -
        CENTER;


    let y =
        event.clientY -
        rect.top -
        CENTER;


    // Only vertical movement matters

    y =
        Math.max(
            -MAX,
            Math.min(
                MAX,
                y
            )
        );


    throttle =
        -y /
        MAX;


    // Visual movement

    throttleStick.style.left =
        "66px";


    throttleStick.style.top =
        (
            CENTER +
            y -
            39
        ) +
        "px";


    updateMotors();

}


// ============================================================
// STEERING STICK
// ============================================================

function steeringControl(
    event
) {

    const rect =
        steeringBase
        .getBoundingClientRect();


    let x =
        event.clientX -
        rect.left -
        CENTER;


    let y =
        event.clientY -
        rect.top -
        CENTER;


    // Only horizontal movement matters

    x =
        Math.max(
            -MAX,
            Math.min(
                MAX,
                x
            )
        );


    steering =
        x /
        MAX;


    // Visual movement

    steeringStick.style.left =
        (
            CENTER +
            x -
            39
        ) +
        "px";


    steeringStick.style.top =
        "66px";


    updateMotors();

}


// ============================================================
// THROTTLE EVENTS
// ============================================================

throttleBase.addEventListener(
    "pointerdown",
    function(event) {

        throttleActive =
            true;

        throttleBase.setPointerCapture(
            event.pointerId
        );

        throttleControl(event);

    }
);


throttleBase.addEventListener(
    "pointermove",
    function(event) {

        if (
            throttleActive
        ) {

            throttleControl(event);

        }

    }
);


throttleBase.addEventListener(
    "pointerup",
    function() {

        throttleActive =
            false;

        throttle =
            0;

        resetStick(
            throttleStick
        );

        updateMotors();

    }
);


throttleBase.addEventListener(
    "pointercancel",
    function() {

        throttleActive =
            false;

        throttle =
            0;

        resetStick(
            throttleStick
        );

        updateMotors();

    }
);


// ============================================================
// STEERING EVENTS
// ============================================================

steeringBase.addEventListener(
    "pointerdown",
    function(event) {

        steeringActive =
            true;

        steeringBase.setPointerCapture(
            event.pointerId
        );

        steeringControl(event);

    }
);


steeringBase.addEventListener(
    "pointermove",
    function(event) {

        if (
            steeringActive
        ) {

            steeringControl(event);

        }

    }
);


steeringBase.addEventListener(
    "pointerup",
    function() {

        steeringActive =
            false;

        steering =
            0;

        resetStick(
            steeringStick
        );

        updateMotors();

    }
);


steeringBase.addEventListener(
    "pointercancel",
    function() {

        steeringActive =
            false;

        steering =
            0;

        resetStick(
            steeringStick
        );

        updateMotors();

    }
);


// ============================================================
// SAFETY
// ============================================================

window.addEventListener(
    "blur",
    function() {

        throttle =
            0;

        steering =
            0;

        throttleActive =
            false;

        steeringActive =
            false;

        resetStick(
            throttleStick
        );

        resetStick(
            steeringStick
        );

        stopMotors();

    }
);


</script>

</body>

</html>
"""


controller_html = controller_html.replace(
    "__WEMOS_IP__",
    WEMOS_IP
)


controller_html = controller_html.replace(
    "__SPEED__",
    str(speed)
)


st.iframe(
    controller_html,
    height=540
)


# ============================================================
# EMERGENCY STOP
# ============================================================

st.divider()

st.subheader("🚨 SAFETY")


stop_html = """
<!DOCTYPE html>

<html>

<head>

<style>

body {
    margin:0;
    background:transparent;
}

button {

    width:100%;

    padding:18px;

    border:none;

    border-radius:14px;

    background:#d71920;

    color:white;

    font-size:22px;

    font-weight:bold;

}

</style>

</head>

<body>


<button onclick="stop()">

🛑 EMERGENCY STOP

</button>


<script>

const WEMOS =
    "__WEMOS_IP__";


function stop() {

    fetch(
        "http://" +
        WEMOS +
        "/stop",
        {
            method:"GET",
            cache:"no-store"
        }
    )

    .then(
        function() {

            alert(
                "🛑 THRUSTERS STOPPED"
            );

        }
    )

    .catch(
        function(error) {

            alert(
                "❌ WEMOS NOT REACHABLE"
            );

            console.log(error);

        }
    );

}

</script>

</body>

</html>
"""


stop_html = stop_html.replace(
    "__WEMOS_IP__",
    WEMOS_IP
)


st.iframe(
    stop_html,
    height=80
)


# ============================================================
# CONNECTION INFO
# ============================================================

st.divider()

st.subheader("📡 CONNECTION")

st.code(
    f"""
WEMOS IP
{WEMOS_IP}

Control endpoint
http://{WEMOS_IP}/motors

Stop endpoint
http://{WEMOS_IP}/stop
""",
    language="text"
)


st.caption(
    "SUBMARINE V2 • PROTOTYPE 2 • DRONE CONTROL"
)
