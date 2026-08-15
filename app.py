import streamlit as st


# ============================================================
# CONFIG
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
# PAGE CSS
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

    h3 {
        text-align: center;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
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
    <h3>
    🟢 PROTOTYPE 2 CONTROL SYSTEM
    </h3>
    """,
    unsafe_allow_html=True
)


# ============================================================
# WEMOS BROWSER STATUS
#
# IMPORTANT:
# Python/Streamlit is NOT checking the Wemos.
# The browser running this page checks 192.168.0.9 directly.
# ============================================================

st.subheader("📡 WEMOS CONNECTION")


status_html = """
<!DOCTYPE html>

<html>

<head>

<meta
name="viewport"
content="width=device-width, initial-scale=1">

<style>

body {

    margin: 0;

    background: transparent;

    color: white;

    font-family: Arial;

    text-align: center;

}

#status {

    padding: 12px;

    border-radius: 12px;

    background: #202833;

    font-size: 18px;

    font-weight: bold;

}

</style>

</head>


<body>


<div id="status">

🟡 CHECKING WEMOS...

</div>


<script>


const WEMOS =
    "__WEMOS_IP__";


const status =
    document.getElementById(
        "status"
    );


// ============================================================
// CHECK WEMOS
// ============================================================

function checkWemos() {

    fetch(
        "http://" +
        WEMOS +
        "/",
        {
            method: "GET",
            cache: "no-store"
        }
    )

    .then(
        function(response) {

            if (response.ok) {

                status.innerHTML =
                    "🟢 WEMOS ONLINE — " +
                    WEMOS;

            }

            else {

                status.innerHTML =
                    "🟡 WEMOS RESPONDED — HTTP " +
                    response.status;

            }

        }
    )

    .catch(
        function(error) {

            status.innerHTML =
                "🔴 WEMOS OFFLINE — " +
                WEMOS;

            console.log(
                "Wemos connection error:",
                error
            );

        }
    );

}


// Check immediately

checkWemos();


// Check every 3 seconds

setInterval(
    checkWemos,
    3000
);


</script>


</body>

</html>
"""


status_html = status_html.replace(
    "__WEMOS_IP__",
    WEMOS_IP
)


st.iframe(
    status_html,
    height=65
)


# ============================================================
# REAR CAMERA
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

    margin: 0;

    background: #080b10;

    color: white;

    font-family: Arial;

    text-align: center;

}

video {

    width: 100%;

    max-width: 650px;

    border-radius: 15px;

    background: black;

}

button {

    padding: 14px 22px;

    margin: 10px;

    border: none;

    border-radius: 12px;

    font-size: 17px;

    font-weight: bold;

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

                audio: false

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
# SPEED SLIDER
# ============================================================

st.subheader("🎚️ MOTOR SPEED")


speed = st.slider(
    "Maximum motor speed",
    min_value=0,
    max_value=100,
    value=20,
    step=1
)


st.markdown(
    f"""
    <h2>
    {speed}%
    </h2>
    """,
    unsafe_allow_html=True
)


# ============================================================
# JOYSTICK
# ============================================================

st.subheader("🕹️ THRUSTER CONTROL")


# IMPORTANT:
# This is intentionally NOT an f-string.
# JavaScript { } therefore causes no Python syntax problems.

joystick_html = """
<!DOCTYPE html>

<html>

<head>

<meta
name="viewport"
content="width=device-width, initial-scale=1">

<style>

body {

    margin: 0;

    background: transparent;

    display: flex;

    justify-content: center;

    align-items: center;

    height: 350px;

    touch-action: none;

    user-select: none;

}


#base {

    width: 250px;

    height: 250px;

    border-radius: 50%;

    background: #202833;

    border: 4px solid #3b4654;

    position: relative;

    touch-action: none;

}


#stick {

    width: 80px;

    height: 80px;

    border-radius: 50%;

    background: #4b83ff;

    position: absolute;

    left: 85px;

    top: 85px;

    box-shadow:
        0 0 20px
        rgba(75,131,255,0.5);

}


#label {

    position: absolute;

    width: 100%;

    top: 265px;

    text-align: center;

    color: #aaa;

    font-family: Arial;

    font-size: 14px;

}

</style>

</head>


<body>


<div id="base">

    <div id="stick"></div>

    <div id="label">

        PUSH TO CONTROL

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


const base =
    document.getElementById(
        "base"
    );


const stick =
    document.getElementById(
        "stick"
    );


const CENTER =
    125;


const MAX_DISTANCE =
    85;


let active =
    false;


let lastLeft =
    0;


let lastRight =
    0;


let sendTimer =
    null;


// ============================================================
// SEND MOTOR COMMAND
// ============================================================

function sendMotors(
    left,
    right
) {

    lastLeft =
        Math.round(left);


    lastRight =
        Math.round(right);


    const url =
        "http://" +
        WEMOS +
        "/motors?left=" +
        lastLeft +
        "&right=" +
        lastRight;


    fetch(
        url,
        {
            method: "GET",
            cache: "no-store"
        }
    )

    .then(
        function(response) {

            if (!response.ok) {

                console.log(
                    "Wemos motor error:",
                    response.status
                );

            }

        }
    )

    .catch(
        function(error) {

            console.log(
                "Motor connection error:",
                error
            );

        }
    );

}


// ============================================================
// CONTINUOUS MOTOR UPDATE
// ============================================================

function startSending() {

    if (
        sendTimer !== null
    ) {

        return;

    }


    sendTimer =
        setInterval(
            function() {

                if (
                    active
                ) {

                    sendMotors(
                        lastLeft,
                        lastRight
                    );

                }

            },
            100
        );

}


// ============================================================
// STOP REPEATED COMMANDS
// ============================================================

function stopSending() {

    if (
        sendTimer !== null
    ) {

        clearInterval(
            sendTimer
        );

        sendTimer =
            null;

    }

}


// ============================================================
// STOP MOTORS
// ============================================================

function stopMotors() {

    lastLeft =
        0;


    lastRight =
        0;


    fetch(
        "http://" +
        WEMOS +
        "/stop",
        {
            method: "GET",
            cache: "no-store"
        }
    )

    .catch(
        function(error) {

            console.log(
                "Stop error:",
                error
            );

        }
    );

}


// ============================================================
// JOYSTICK CONTROL
// ============================================================

function control(
    x,
    y
) {


    // ========================================================
    // LIMIT STICK TO CIRCLE
    // ========================================================

    const distance =
        Math.sqrt(
            x * x +
            y * y
        );


    if (
        distance >
        MAX_DISTANCE
    ) {

        x =
            x /
            distance *
            MAX_DISTANCE;


        y =
            y /
            distance *
            MAX_DISTANCE;

    }


    // ========================================================
    // MOVE VISUAL STICK
    // ========================================================

    stick.style.left =
        (
            CENTER +
            x -
            40
        ) +
        "px";


    stick.style.top =
        (
            CENTER +
            y -
            40
        ) +
        "px";


    // ========================================================
    // THROTTLE
    // ========================================================

    let throttle =
        -y /
        MAX_DISTANCE;


    // ========================================================
    // STEERING
    // ========================================================

    let steering =
        x /
        MAX_DISTANCE;


    // ========================================================
    // DEADZONE
    // ========================================================

    const DEADZONE =
        0.08;


    if (
        Math.abs(throttle) <
        DEADZONE
    ) {

        throttle =
            0;

    }


    if (
        Math.abs(steering) <
        DEADZONE
    ) {

        steering =
            0;

    }


    // ========================================================
    // DIFFERENTIAL THRUSTER MIXING
    //
    // Forward:
    //
    // left  = +
    // right = +
    //
    // Back:
    //
    // left  = -
    // right = -
    //
    // Turn:
    //
    // left  = +
    // right = -
    // ========================================================

    let left =
        throttle +
        steering;


    let right =
        throttle -
        steering;


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
    // APPLY SPEED SLIDER
    // ========================================================

    left =
        left *
        SPEED;


    right =
        right *
        SPEED;


    // ========================================================
    // SAVE
    // ========================================================

    lastLeft =
        left;


    lastRight =
        right;


    // ========================================================
    // SEND IMMEDIATELY
    // ========================================================

    sendMotors(
        left,
        right
    );

}


// ============================================================
// RELEASE JOYSTICK
// ============================================================

function release() {

    active =
        false;


    stopSending();


    stick.style.left =
        "85px";


    stick.style.top =
        "85px";


    stopMotors();

}


// ============================================================
// POINTER DOWN
// ============================================================

base.addEventListener(
    "pointerdown",

    function(event) {

        active =
            true;


        base.setPointerCapture(
            event.pointerId
        );


        const rect =
            base.getBoundingClientRect();


        control(

            event.clientX -
            rect.left -
            CENTER,

            event.clientY -
            rect.top -
            CENTER

        );


        startSending();

    }

);


// ============================================================
// POINTER MOVE
// ============================================================

base.addEventListener(
    "pointermove",

    function(event) {

        if (
            !active
        ) {

            return;

        }


        const rect =
            base.getBoundingClientRect();


        control(

            event.clientX -
            rect.left -
            CENTER,

            event.clientY -
            rect.top -
            CENTER

        );

    }

);


// ============================================================
// POINTER UP
// ============================================================

base.addEventListener(
    "pointerup",

    function() {

        release();

    }

);


// ============================================================
// POINTER CANCEL
// ============================================================

base.addEventListener(
    "pointercancel",

    function() {

        release();

    }

);


// ============================================================
// EXTRA SAFETY
// ============================================================

window.addEventListener(
    "blur",

    function() {

        if (
            active
        ) {

            release();

        }

    }

);


</script>


</body>

</html>
"""


# ============================================================
# INSERT CONFIG VALUES
# ============================================================

joystick_html = joystick_html.replace(
    "__WEMOS_IP__",
    WEMOS_IP
)


joystick_html = joystick_html.replace(
    "__SPEED__",
    str(speed)
)


st.iframe(
    joystick_html,
    height=370
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

    margin: 0;

    font-family: Arial;

    text-align: center;

}

button {

    width: 100%;

    padding: 18px;

    border: none;

    border-radius: 14px;

    background: #d71920;

    color: white;

    font-size: 22px;

    font-weight: bold;

}

</style>

</head>


<body>


<button onclick="emergencyStop()">

🛑 EMERGENCY STOP

</button>


<script>


const WEMOS =
    "__WEMOS_IP__";


function emergencyStop() {

    fetch(
        "http://" +
        WEMOS +
        "/stop",
        {
            method: "GET",
            cache: "no-store"
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

            console.log(
                error
            );

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
# CONNECTION INFORMATION
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
    "Prototype 2 • Wemos D1 R1 • Wi-Fi control"
)
