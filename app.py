import streamlit as st


# ============================================================
# WEMOS CONFIG
# ============================================================

WEMOS_IP = "192.168.0.9"


# ============================================================
# PAGE CONFIG
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
        background:#080b10;
        color:white;
    }

    h1 {
        text-align:center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "⚓ SUBMARINE V2"
)

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

st.subheader(
    "📹 REAR CAMERA"
)


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

    text-align:center;

    font-family:Arial;

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

                        ideal:"environment"

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

st.subheader(
    "🎚️ MASTER SPEED"
)


speed = st.slider(
    "Maximum motor speed",
    0,
    100,
    20,
    1
)


st.markdown(
    f"""
    <h2 style="text-align:center;">
    {speed}%
    </h2>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONTROLLER
# ============================================================

st.subheader(
    "🎮 DRONE CONTROL"
)


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

    touch-action:none;

    user-select:none;

    font-family:Arial;

}


#controller {

    height:500px;

    width:100%;

    display:flex;

    justify-content:space-around;

    align-items:center;

}


.area {

    width:250px;

    height:330px;

    position:relative;

    display:flex;

    justify-content:center;

    align-items:center;

}


.base {

    width:210px;

    height:210px;

    border-radius:50%;

    background:#202833;

    border:5px solid #3b4654;

    position:relative;

    touch-action:none;

}


.stick {

    width:76px;

    height:76px;

    border-radius:50%;

    background:#4b83ff;

    position:absolute;

    left:67px;

    top:67px;

    box-shadow:
        0 0 25px
        rgba(75,131,255,.5);

    pointer-events:none;

}


.label {

    position:absolute;

    bottom:5px;

    width:100%;

    text-align:center;

    color:#aaa;

    font-weight:bold;

}


.direction {

    position:absolute;

    color:#777;

    font-size:22px;

    font-weight:bold;

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


#status {

    text-align:center;

    color:#00ff66;

    font-weight:bold;

    height:25px;

}

</style>

</head>


<body>


<div id="status">
🟢 READY
</div>


<div id="controller">


<!-- ========================================================
     THROTTLE JOYSTICK
     ======================================================== -->

<div class="area">


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
     STEERING JOYSTICK
     ======================================================== -->

<div class="area">


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


const CENTER =
    105;


const MAX =
    65;


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
// CONTROL VALUES
// ============================================================

let throttle = 0;

let steering = 0;

let throttleActive = false;

let steeringActive = false;


// ============================================================
// SEND MOTOR COMMAND
// ============================================================

function sendMotors(
    left,
    right
) {

    left =
        Math.round(left);

    right =
        Math.round(right);


    const url =
        "http://" +
        WEMOS +
        "/motors?left=" +
        left +
        "&right=" +
        right;


    fetch(
        url,
        {
            cache:"no-store"
        }
    )

    .then(
        function(response) {

            if (
                response.ok
            ) {

                status.innerText =
                    "🟢 L " +
                    left +
                    "%   R " +
                    right +
                    "%";

            }

        }
    )

    .catch(
        function() {

            status.innerText =
                "🔴 CONNECTION ERROR";

        }
    );

}


// ============================================================
// MOTOR MIXER
// ============================================================

function updateMotors() {


    let t =
        throttle;


    let s =
        steering;


    let left;

    let right;


    // ========================================================
    // NO FORWARD/BACKWARD
    // ========================================================

    if (
        Math.abs(t) < 0.01
    ) {


        // Small pivot control only

        left =
            -s * 0.20;


        right =
            s * 0.20;

    }


    // ========================================================
    // MOVING
    // ========================================================

    else {


        /*
         * Steering changes the amount of thrust
         * on each side.
         *
         * Both motors remain in the SAME
         * physical direction.
         */

        const turn =
            Math.abs(t) * s;


        left =
            t - turn;


        right =
            t + turn;

    }


    // ========================================================
    // LIMIT
    // ========================================================

    left =
        Math.max(
            -1,
            Math.min(
                1,
                left
            )
        );


    right =
        Math.max(
            -1,
            Math.min(
                1,
                right
            )
        );


    // ========================================================
    // SPEED
    // ========================================================

    left =
        left * SPEED;


    right =
        right * SPEED;


    sendMotors(
        left,
        right
    );

}


// ============================================================
// THROTTLE
// ============================================================

function moveThrottle(
    event
) {


    const rect =
        throttleBase
        .getBoundingClientRect();


    let y =
        event.clientY -
        rect.top -
        CENTER;


    y =
        Math.max(
            -MAX,
            Math.min(
                MAX,
                y
            )
        );


    throttle =
        -y / MAX;


    throttleStick.style.left =
        "67px";


    throttleStick.style.top =
        (
            CENTER +
            y -
            38
        ) +
        "px";


    updateMotors();

}


// ============================================================
// STEERING
// ============================================================

function moveSteering(
    event
) {


    const rect =
        steeringBase
        .getBoundingClientRect();


    let x =
        event.clientX -
        rect.left -
        CENTER;


    x =
        Math.max(
            -MAX,
            Math.min(
                MAX,
                x
            )
        );


    steering =
        x / MAX;


    steeringStick.style.left =
        (
            CENTER +
            x -
            38
        ) +
        "px";


    steeringStick.style.top =
        "67px";


    updateMotors();

}


// ============================================================
// RESET THROTTLE
// ============================================================

function resetThrottle() {

    throttle =
        0;


    throttleActive =
        false;


    throttleStick.style.left =
        "67px";


    throttleStick.style.top =
        "67px";


    updateMotors();

}


// ============================================================
// RESET STEERING
// ============================================================

function resetSteering() {

    steering =
        0;


    steeringActive =
        false;


    steeringStick.style.left =
        "67px";


    steeringStick.style.top =
        "67px";


    updateMotors();

}


// ============================================================
// THROTTLE POINTER
// ============================================================

throttleBase.addEventListener(
    "pointerdown",
    function(event) {


        throttleActive =
            true;


        throttleBase.setPointerCapture(
            event.pointerId
        );


        moveThrottle(
            event
        );

    }
);


throttleBase.addEventListener(
    "pointermove",
    function(event) {


        if (
            throttleActive
        ) {

            moveThrottle(
                event
            );

        }

    }
);


throttleBase.addEventListener(
    "pointerup",
    resetThrottle
);


throttleBase.addEventListener(
    "pointercancel",
    resetThrottle
);


// ============================================================
// STEERING POINTER
// ============================================================

steeringBase.addEventListener(
    "pointerdown",
    function(event) {


        steeringActive =
            true;


        steeringBase.setPointerCapture(
            event.pointerId
        );


        moveSteering(
            event
        );

    }
);


steeringBase.addEventListener(
    "pointermove",
    function(event) {


        if (
            steeringActive
        ) {

            moveSteering(
                event
            );

        }

    }
);


steeringBase.addEventListener(
    "pointerup",
    resetSteering
);


steeringBase.addEventListener(
    "pointercancel",
    resetSteering
);


// ============================================================
// CONTINUOUS HEARTBEAT
// ============================================================
//
// IMPORTANT:
//
// The Wemos has a 1.5 second safety timeout.
//
// While either joystick is held,
// keep sending the current motor values.
//

setInterval(
    function() {


        if (
            throttleActive ||
            steeringActive
        ) {

            updateMotors();

        }

    },
    200
);


// ============================================================
// PHONE/TAB SAFETY
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


        throttleStick.style.left =
            "67px";


        throttleStick.style.top =
            "67px";


        steeringStick.style.left =
            "67px";


        steeringStick.style.top =
            "67px";


        fetch(
            "http://" +
            WEMOS +
            "/stop"
        )
        .catch(
            function() {}
        );

    }
);


</script>


</body>

</html>
"""


# ============================================================
# INSERT CONFIG
# ============================================================

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


st.subheader(
    "🚨 SAFETY"
)


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
            cache:"no-store"
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


st.subheader(
    "📡 WEMOS CONNECTION"
)


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
