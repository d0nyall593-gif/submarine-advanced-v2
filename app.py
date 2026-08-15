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

    h3 {
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
    <h3>
    🟢 PROTOTYPE 2 CONTROL SYSTEM
    </h3>
    """,
    unsafe_allow_html=True
)


# ============================================================
# WEMOS STATUS
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
                    "🟡 WEMOS HTTP " +
                    response.status;

            }

        }
    )

    .catch(
        function(error) {

            status.innerHTML =
                "🔴 WEMOS OFFLINE — " +
                WEMOS;

            console.log(error);

        }
    );

}


checkWemos();


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
# SPEED
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
    f"<h2>{speed}%</h2>",
    unsafe_allow_html=True
)


# ============================================================
# JOYSTICK
# ============================================================

st.subheader("🕹️ THRUSTER CONTROL")


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


const SEND_INTERVAL =
    100;


let active =
    false;


let lastLeft =
    0;


let lastRight =
    0;


let sendTimer =
    null;


// ============================================================
// SEND
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

    .catch(
        function(error) {

            console.log(
                "Motor error:",
                error
            );

        }
    );

}


// ============================================================
// CONTINUOUS SEND
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

                if (active) {

                    sendMotors(
                        lastLeft,
                        lastRight
                    );

                }

            },
            SEND_INTERVAL
        );

}


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
// STOP
// ============================================================

function stopMotors() {

    lastLeft = 0;
    lastRight = 0;


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
// JOYSTICK
// ============================================================

function control(
    x,
    y
) {

    const distance =
        Math.sqrt(
            x * x +
            y * y
        );


    // Keep stick inside circle

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


    // Visual stick

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

        throttle = 0;

    }


    if (
        Math.abs(steering) <
        DEADZONE
    ) {

        steering = 0;

    }


    // ========================================================
    // SMOOTH STEERING
    //
    // THIS IS THE IMPORTANT CHANGE.
    //
    // The motors do NOT immediately reverse against each other
    // when steering.
    //
    // Forward + LEFT:
    //     left  slows
    //     right stays faster
    //
    // Forward + RIGHT:
    //     right slows
    //     left stays faster
    //
    // This feels much more like normal steering.
    // ========================================================

    let left =
        throttle *
        (1 - steering);


    let right =
        throttle *
        (1 + steering);


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


    // Send immediately

    sendMotors(
        left,
        right
    );

}


// ============================================================
// RELEASE
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

        if (!active) {

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
// RELEASE
// ============================================================

base.addEventListener(
    "pointerup",
    release
);


base.addEventListener(
    "pointercancel",
    release
);


// Extra safety

window.addEventListener(
    "blur",
    function() {

        if (active) {

            release();

        }

    }
);


</script>


</body>

</html>
"""


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
        "/stop"
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
# CONNECTION INFO
# ============================================================

st.divider()

st.subheader("📡 CONNECTION")

st.code(
    f"""
WEMOS IP
{WEMOS_IP}

Motor endpoint
http://{WEMOS_IP}/motors

Stop endpoint
http://{WEMOS_IP}/stop
""",
    language="text"
)


st.caption(
    "SUBMARINE V2 • PROTOTYPE 2"
)
