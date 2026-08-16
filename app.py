import streamlit as st
import streamlit.components.v1 as components
import requests
import time


# ============================================================
# WEMOS CONFIG
# ============================================================

WEMOS_IP = "192.168.0.9"

WEMOS_URL = f"http://{WEMOS_IP}"

MOTOR_ENDPOINT = f"{WEMOS_URL}/motors"

STOP_ENDPOINT = f"{WEMOS_URL}/stop"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SUBMARINE V2",
    page_icon="⚓",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# MOBILE CSS
# ============================================================

st.markdown(
    """
    <style>

    html, body {
        margin: 0;
        padding: 0;
        background: #070b10;
    }

    .stApp {
        background: #070b10;
        color: white;
    }

    .block-container {
        max-width: 700px;
        padding-top: 0.6rem;
        padding-left: 0.7rem;
        padding-right: 0.7rem;
        padding-bottom: 2rem;
    }

    h1 {
        text-align: center;
        margin-bottom: 0.2rem;
    }

    h2, h3 {
        text-align: center;
    }

    div.stButton > button {
        min-height: 55px;
        border-radius: 15px;
        font-size: 18px;
        font-weight: bold;
    }

    @media (max-width: 600px) {

        .block-container {
            padding-left: 8px;
            padding-right: 8px;
        }

        h1 {
            font-size: 28px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TITLE
# ============================================================

st.title("⚓ SUBMARINE V2")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#63ff7a;
        font-size:16px;
        margin-bottom:12px;
    ">
        🟢 MOBILE CONTROL SYSTEM
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# WEMOS STATUS
# ============================================================

try:

    response = requests.get(
        WEMOS_URL,
        timeout=1.5
    )

    if response.status_code == 200:

        st.success(
            f"🟢 WEMOS ONLINE — {WEMOS_IP}"
        )

    else:

        st.warning(
            f"🟡 WEMOS RESPONDED — HTTP {response.status_code}"
        )

except requests.RequestException:

    st.error(
        f"🔴 WEMOS OFFLINE — {WEMOS_IP}"
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

html, body {

    margin: 0;
    padding: 0;

    background: #070b10;

    color: white;

    font-family: Arial;

    text-align: center;

}

.camera-container {

    width: 100%;

    max-width: 650px;

    margin: auto;

}

video {

    width: 100%;

    height: auto;

    min-height: 230px;

    max-height: 430px;

    object-fit: cover;

    background: black;

    border-radius: 16px;

    border: 2px solid #27313d;

}

button {

    width: 90%;

    max-width: 400px;

    padding: 14px;

    margin-top: 12px;

    border: none;

    border-radius: 14px;

    background: #202833;

    color: white;

    font-size: 17px;

    font-weight: bold;

}

button:active {

    transform: scale(0.97);

}

#status {

    margin-top: 8px;

    font-size: 14px;

    color: #9aa6b2;

}

</style>

</head>


<body>

<div class="camera-container">

<video
id="camera"
autoplay
playsinline>
</video>

<button onclick="startCamera()">
📹 START REAR CAMERA
</button>

<div id="status">
Camera waiting...
</div>

</div>


<script>

async function startCamera() {

    const status =
        document.getElementById("status");

    try {

        const stream =
            await navigator.mediaDevices.getUserMedia({

                video: {

                    facingMode: {
                        ideal: "environment"
                    },

                    width: {
                        ideal: 1280
                    },

                    height: {
                        ideal: 720
                    }

                },

                audio: false

            });

        document.getElementById(
            "camera"
        ).srcObject = stream;

        status.innerText =
            "🟢 REAR CAMERA ACTIVE";

    }

    catch(error) {

        status.innerText =
            "🔴 CAMERA ERROR: " +
            error.message;

    }

}

</script>

</body>

</html>
"""


components.html(
    camera_html,
    height=470,
    scrolling=False
)


# ============================================================
# SPEED
# ============================================================

st.subheader("🎚️ MOTOR SPEED")


speed = st.slider(
    "Maximum motor power",
    min_value=0,
    max_value=100,
    value=20,
    step=1,
    key="motor_speed"
)


st.markdown(
    f"""
    <div style="
        text-align:center;
        font-size:28px;
        font-weight:bold;
        margin-top:-5px;
        margin-bottom:10px;
    ">
        {speed}%
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MOBILE DRONE CONTROLLER
# ============================================================

st.subheader("🕹️ DRONE CONTROL")


# IMPORTANT:
# This is NOT a Python f-string.
# Therefore JavaScript braces do NOT need escaping.

controller_html = """
<!DOCTYPE html>

<html>

<head>

<meta
name="viewport"
content="width=device-width, initial-scale=1">

<style>

html, body {

    margin: 0;
    padding: 0;

    width: 100%;

    background: transparent;

    color: white;

    font-family: Arial;

    user-select: none;

    -webkit-user-select: none;

    touch-action: none;

}

#controller {

    width: 100%;

    max-width: 680px;

    margin: auto;

    touch-action: none;

}

#sticks {

    display: flex;

    justify-content: space-between;

    align-items: center;

    gap: 15px;

    padding: 10px;

}

.stick-area {

    width: 46vw;

    max-width: 270px;

    height: 270px;

    max-height: 270px;

    position: relative;

    touch-action: none;

}

.base {

    position: absolute;

    width: 100%;

    height: 100%;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            #283341 0%,
            #1a222c 65%,
            #11171e 100%
        );

    border: 4px solid #3d4b5b;

    box-sizing: border-box;

    box-shadow:
        inset 0 0 25px #080b10,
        0 0 15px rgba(0,0,0,0.5);

    touch-action: none;

}

.cross-h {

    position: absolute;

    left: 15%;

    right: 15%;

    top: 50%;

    height: 1px;

    background: #526170;

    opacity: 0.5;

}

.cross-v {

    position: absolute;

    top: 15%;

    bottom: 15%;

    left: 50%;

    width: 1px;

    background: #526170;

    opacity: 0.5;

}

.knob {

    position: absolute;

    width: 78px;

    height: 78px;

    left: 50%;

    top: 50%;

    transform:
        translate(-50%, -50%);

    border-radius: 50%;

    background:
        radial-gradient(
            circle at 35% 30%,
            #78a9ff,
            #3269db 55%,
            #204b9d
        );

    border: 3px solid #86b0ff;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.5),
        0 0 20px rgba(65,125,255,0.35);

    touch-action: none;

}

.label {

    text-align: center;

    font-size: 14px;

    color: #aab6c3;

    margin-top: 5px;

}

#telemetry {

    text-align: center;

    margin-top: 8px;

    padding: 10px;

    background: #111820;

    border-radius: 12px;

    font-size: 14px;

    color: #b7c3cf;

}

#connection {

    color: #63ff7a;

}

</style>

</head>


<body>


<div id="controller">


<div id="sticks">


<!-- LEFT STICK -->

<div>

<div
class="stick-area"
id="leftArea">

<div class="base">

<div class="cross-h"></div>

<div class="cross-v"></div>

<div
class="knob"
id="leftKnob">
</div>

</div>

</div>

<div class="label">
LEFT — THROTTLE / YAW
</div>

</div>


<!-- RIGHT STICK -->

<div>

<div
class="stick-area"
id="rightArea">

<div class="base">

<div class="cross-h"></div>

<div class="cross-v"></div>

<div
class="knob"
id="rightKnob">
</div>

</div>

</div>

<div class="label">
RIGHT — THROTTLE / STEERING
</div>

</div>


</div>


<div id="telemetry">

<div id="connection">
🟢 CONTROLLER READY
</div>

<div>
LEFT MOTOR:
<span id="leftValue">0</span>%
</div>

<div>
RIGHT MOTOR:
<span id="rightValue">0</span>%
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
// STATE
// ============================================================

let leftX = 0;

let leftY = 0;

let rightX = 0;

let rightY = 0;

let leftActive = false;

let rightActive = false;


// ============================================================
// MOTOR STATE
// ============================================================

let currentLeft = 0;

let currentRight = 0;


// ============================================================
// SEND MOTOR COMMAND
// ============================================================

let lastSend = 0;

const SEND_INTERVAL = 80;


function sendMotors(left, right) {

    const now =
        Date.now();

    if (
        now - lastSend <
        SEND_INTERVAL
    ) {

        return;

    }

    lastSend = now;


    currentLeft =
        Math.round(left);

    currentRight =
        Math.round(right);


    document.getElementById(
        "leftValue"
    ).innerText =
        currentLeft;


    document.getElementById(
        "rightValue"
    ).innerText =
        currentRight;


    const url =
        "http://" +
        WEMOS +
        "/motors?left=" +
        currentLeft +
        "&right=" +
        currentRight;


    fetch(
        url,
        {
            method: "GET",
            cache: "no-store"
        }
    )

    .then(function(response) {

        if (!response.ok) {

            document.getElementById(
                "connection"
            ).innerText =
                "🔴 WEMOS ERROR";

        }

        else {

            document.getElementById(
                "connection"
            ).innerText =
                "🟢 CONTROL LINK ACTIVE";

        }

    })

    .catch(function() {

        document.getElementById(
            "connection"
        ).innerText =
            "🔴 CONTROL LINK LOST";

    });

}


// ============================================================
// STOP
// ============================================================

function stopMotors() {

    currentLeft = 0;

    currentRight = 0;


    document.getElementById(
        "leftValue"
    ).innerText = "0";


    document.getElementById(
        "rightValue"
    ).innerText = "0";


    fetch(
        "http://" +
        WEMOS +
        "/stop",
        {
            method: "GET",
            cache: "no-store"
        }
    ).catch(function() {});

}


// ============================================================
// MIXING
// ============================================================
//
// RIGHT STICK:
// Y = forward/backward
// X = steering
//
// This produces:
//
// forward:
// left  +
// right +
//
// backward:
// left  -
// right -
//
// right:
// left  +
// right -
//
// left:
// left  -
// right +
//
// ============================================================

function updateMotors() {

    let throttle =
        -rightY;

    let steering =
        rightX;


    let left =
        throttle +
        steering;


    let right =
        throttle -
        steering;


    // Normalize

    const maxValue =
        Math.max(
            1,
            Math.abs(left),
            Math.abs(right)
        );


    left =
        left /
        maxValue;


    right =
        right /
        maxValue;


    // Apply speed

    left =
        left *
        SPEED;


    right =
        right *
        SPEED;


    sendMotors(
        left,
        right
    );

}


// ============================================================
// CREATE STICK
// ============================================================

function setupStick(
    areaId,
    knobId,
    callback
) {

    const area =
        document.getElementById(
            areaId
        );

    const knob =
        document.getElementById(
            knobId
        );


    let active = false;


    function move(
        clientX,
        clientY
    ) {

        const rect =
            area.getBoundingClientRect();


        const centerX =
            rect.width / 2;


        const centerY =
            rect.height / 2;


        let x =
            clientX -
            rect.left -
            centerX;


        let y =
            clientY -
            rect.top -
            centerY;


        const radius =
            rect.width / 2;


        const distance =
            Math.sqrt(
                x * x +
                y * y
            );


        if (
            distance > radius
        ) {

            x =
                x /
                distance *
                radius;

            y =
                y /
                distance *
                radius;

        }


        // Normalize -1 to +1

        const nx =
            x / radius;

        const ny =
            y / radius;


        // Move knob

        knob.style.left =
            (
                50 +
                nx * 34
            ) + "%";


        knob.style.top =
            (
                50 +
                ny * 34
            ) + "%";


        callback(
            nx,
            ny
        );

    }


    function reset() {

        active = false;


        knob.style.left =
            "50%";


        knob.style.top =
            "50%";


        callback(
            0,
            0
        );

    }


    area.addEventListener(
        "pointerdown",
        function(event) {

            active = true;

            area.setPointerCapture(
                event.pointerId
            );


            move(
                event.clientX,
                event.clientY
            );

        }
    );


    area.addEventListener(
        "pointermove",
        function(event) {

            if (!active) {

                return;

            }


            move(
                event.clientX,
                event.clientY
            );

        }
    );


    area.addEventListener(
        "pointerup",
        function() {

            reset();

        }
    );


    area.addEventListener(
        "pointercancel",
        function() {

            reset();

        }
    );

}


// ============================================================
// LEFT STICK
// ============================================================
//
// Kept available for drone-style control.
// Currently used as yaw input.
//
// ============================================================

setupStick(
    "leftArea",
    "leftKnob",
    function(x, y) {

        leftX = x;

        leftY = y;

        // Left stick adds gentle yaw control

        if (
            !rightActive
        ) {

            rightX =
                leftX;

            rightY =
                leftY;

        }

        updateMotors();

    }
);


// ============================================================
// RIGHT STICK
// ============================================================

setupStick(
    "rightArea",
    "rightKnob",
    function(x, y) {

        rightX = x;

        rightY = y;

        updateMotors();

    }
);


// ============================================================
// SAFETY
// ============================================================

window.addEventListener(
    "blur",
    function() {

        leftX = 0;
        leftY = 0;

        rightX = 0;
        rightY = 0;

        stopMotors();

    }
);


document.addEventListener(
    "visibilitychange",
    function() {

        if (
            document.hidden
        ) {

            stopMotors();

        }

    }
);


// ============================================================
// START HEARTBEAT
// ============================================================

setInterval(
    function() {

        if (
            leftActive ||
            rightActive
        ) {

            updateMotors();

        }

    },
    100
);


</script>


</body>

</html>
"""


# Replace placeholders instead of using a giant f-string.
controller_html = controller_html.replace(
    "__WEMOS_IP__",
    WEMOS_IP
)

controller_html = controller_html.replace(
    "__SPEED__",
    str(speed)
)


components.html(
    controller_html,
    height=390,
    scrolling=False
)


# ============================================================
# EMERGENCY STOP
# ============================================================

st.divider()


if st.button(
    "🛑 EMERGENCY STOP",
    use_container_width=True,
    type="primary"
):

    try:

        requests.get(
            STOP_ENDPOINT,
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
# WEMOS TEST
# ============================================================

with st.expander("📡 WEMOS CONNECTION TEST"):

    if st.button(
        "TEST WEMOS",
        use_container_width=True
    ):

        try:

            response = requests.get(
                WEMOS_URL,
                timeout=2
            )


            if response.status_code == 200:

                st.success(
                    "🟢 WEMOS ONLINE"
                )

                st.code(
                    response.text
                )

            else:

                st.warning(
                    f"Wemos returned HTTP "
                    f"{response.status_code}"
                )


        except requests.RequestException as error:

            st.error(
                f"Connection failed: {error}"
            )


# ============================================================
# END
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#66727f;
        font-size:12px;
        margin-top:20px;
    ">
        SUBMARINE V2 • MOBILE CONTROL
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "SUBMARINE V2 • PROTOTYPE 2 • DRONE CONTROL"
)
