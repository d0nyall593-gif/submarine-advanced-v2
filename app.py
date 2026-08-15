import streamlit as st
import requests


# ============================================================
# WEMOS CONFIG
# ============================================================

WEMOS_IP = "192.168.0.9"
WEMOS_URL = f"http://{WEMOS_IP}"


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

st.markdown("""
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
""", unsafe_allow_html=True)


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

try:

    response = requests.get(
        WEMOS_URL,
        timeout=0.7
    )

    if response.status_code == 200:

        st.success(
            f"🟢 WEMOS ONLINE — {WEMOS_IP}"
        )

    else:

        st.warning(
            f"🟡 WEMOS RESPONDED — "
            f"HTTP {response.status_code}"
        )

except requests.RequestException:

    st.error(
        f"🔴 WEMOS OFFLINE — {WEMOS_IP}"
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
    text-align: center;
    font-family: Arial;
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
            await navigator.mediaDevices.getUserMedia({

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


# IMPORTANT:
# This is NOT an f-string.
# Therefore JavaScript { } do not need escaping.

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

    height: 340px;

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

</style>

</head>


<body>


<div id="base">

    <div id="stick"></div>

</div>


<script>


// ============================================================
// CONFIG
// ============================================================

const WEMOS = "__WEMOS_IP__";

const SPEED = __SPEED__;


const base =
    document.getElementById("base");


const stick =
    document.getElementById("stick");


const CENTER = 125;

const MAX_DISTANCE = 85;


// Send commands every 100 ms

const SEND_INTERVAL = 100;


let active = false;

let lastLeft = 0;

let lastRight = 0;

let sendTimer = null;


// ============================================================
// SEND MOTOR COMMAND
// ============================================================

function sendMotors(left, right) {

    const url =
        "http://" +
        WEMOS +
        "/motors?left=" +
        Math.round(left) +
        "&right=" +
        Math.round(right);


    fetch(url)

        .then(function(response) {

            if (!response.ok) {

                console.log(
                    "Wemos error:",
                    response.status
                );

            }

        })

        .catch(function(error) {

            console.log(
                "Wemos connection error:",
                error
            );

        });

}


// ============================================================
// REPEATED COMMAND SENDER
// ============================================================

function startSending() {

    if (sendTimer !== null) {

        return;

    }


    sendTimer = setInterval(
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


// ============================================================
// STOP REPEATED SENDING
// ============================================================

function stopSending() {

    if (sendTimer !== null) {

        clearInterval(
            sendTimer
        );

        sendTimer = null;

    }

}


// ============================================================
// STOP MOTORS
// ============================================================

function stopMotors() {

    lastLeft = 0;

    lastRight = 0;


    fetch(
        "http://" +
        WEMOS +
        "/stop"
    )

    .catch(function(error) {

        console.log(
            "Stop error:",
            error
        );

    });

}


// ============================================================
// JOYSTICK CONTROL
// ============================================================

function control(x, y) {

    const distance =
        Math.sqrt(
            x * x +
            y * y
        );


    // Keep stick inside circle

    if (
        distance > MAX_DISTANCE
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
    // VISUAL STICK
    // ========================================================

    stick.style.left =
        (
            CENTER +
            x -
            40
        ) + "px";


    stick.style.top =
        (
            CENTER +
            y -
            40
        ) + "px";


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
    // DIFFERENTIAL MIXING
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
    // SPEED LIMIT
    // ========================================================

    left =
        left *
        SPEED;


    right =
        right *
        SPEED;


    // ========================================================
    // SAVE CURRENT COMMAND
    // ========================================================

    lastLeft = left;

    lastRight = right;


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

    active = false;

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

        active = true;


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

        if (active) {

            release();

        }

    }

);


</script>


</body>

</html>
"""


# ============================================================
# INSERT PYTHON VALUES
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
    height=360
)


# ============================================================
# EMERGENCY STOP
# ============================================================

st.divider()


if st.button(
    "🛑 EMERGENCY STOP",
    use_container_width=True
):

    try:

        requests.get(
            f"{WEMOS_URL}/stop",
            timeout=1
        )


        st.success(
            "🛑 THRUSTERS STOPPED"
        )

    except requests.RequestException:

        st.error(
            "❌ WEMOS NOT REACHABLE"
        )


# ============================================================
# TEST WEMOS
# ============================================================

if st.button(
    "📡 TEST WEMOS",
    use_container_width=True
):

    try:

        response = requests.get(
            WEMOS_URL,
            timeout=1
        )


        if response.status_code == 200:

            st.success(
                "🟢 WEMOS ONLINE!"
            )

            st.code(
                response.text
            )

        else:

            st.error(
                f"Wemos HTTP error: "
                f"{response.status_code}"
            )


    except requests.RequestException as error:

        st.error(
            f"Connection failed: {error}"
        )
