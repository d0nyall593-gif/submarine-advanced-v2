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

.status {
    text-align: center;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.title("⚓ SUBMARINE V2")

st.markdown(
    '<div class="status">🟢 PROTOTYPE 2 CONTROL SYSTEM</div>',
    unsafe_allow_html=True
)


# ============================================================
# WEMOS CONNECTION
# ============================================================

try:

    response = requests.get(
        WEMOS_URL,
        timeout=0.5
    )

    wemos_online = response.status_code == 200

except requests.RequestException:

    wemos_online = False


if wemos_online:

    st.success(
        "🟢 WEMOS ONLINE — 192.168.0.9"
    )

else:

    st.error(
        "🔴 WEMOS OFFLINE — 192.168.0.9"
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

    max-width: 600px;

    border-radius: 15px;

    background: black;

}

button {

    padding: 12px 20px;

    margin: 10px;

    border-radius: 10px;

    border: none;

    font-size: 16px;

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
            "Camera error: "
            + error.message
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


joystick_html = f"""
<!DOCTYPE html>

<html>

<head>

<meta
name="viewport"
content="width=device-width, initial-scale=1">

<style>

body {{

    margin: 0;

    background: transparent;

    display: flex;

    justify-content: center;

    align-items: center;

    height: 330px;

    touch-action: none;

}}


#base {{

    width: 240px;

    height: 240px;

    border-radius: 50%;

    background: #202833;

    border: 4px solid #3b4654;

    position: relative;

    touch-action: none;

}}


#stick {{

    width: 80px;

    height: 80px;

    border-radius: 50%;

    background: #4b83ff;

    position: absolute;

    left: 80px;

    top: 80px;

    box-shadow:
        0 0 20px rgba(75,131,255,0.5);

}}

</style>

</head>


<body>


<div id="base">

    <div id="stick"></div>

</div>


<script>


// ============================================================
// WEMOS
// ============================================================

const WEMOS =
    "{WEMOS_IP}";


const base =
    document.getElementById("base");


const stick =
    document.getElementById("stick");


const center = 120;

const maxDistance = 80;

let active = false;


// ============================================================
// SEND MOTOR COMMAND
// ============================================================

function sendMotors(left, right) {{

    fetch(
        "http://" +
        WEMOS +
        "/motors?left=" +
        Math.round(left) +
        "&right=" +
        Math.round(right)
    )
    .catch(function(error) {{

        console.log(
            "Wemos connection error:",
            error
        );

    }});

}}


// ============================================================
// JOYSTICK CONTROL
// ============================================================

function control(x, y) {{

    const distance =
        Math.sqrt(
            x * x +
            y * y
        );


    // Keep stick inside circle

    if (
        distance > maxDistance
    ) {{

        x =
            x /
            distance *
            maxDistance;

        y =
            y /
            distance *
            maxDistance;

    }}


    // Move visual stick

    stick.style.left =
        (
            center +
            x -
            40
        ) + "px";


    stick.style.top =
        (
            center +
            y -
            40
        ) + "px";


    // ========================================================
    // THROTTLE
    // ========================================================

    // Up = positive throttle
    // Down = negative throttle

    let throttle =
        -y / maxDistance;


    // ========================================================
    // STEERING
    // ========================================================

    let steering =
        x / maxDistance;


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
        {speed};


    right =
        right *
        {speed};


    // ========================================================
    // SEND
    // ========================================================

    sendMotors(
        left,
        right
    );

}}


// ============================================================
// RELEASE JOYSTICK
// ============================================================

function release() {{

    active = false;


    // Return stick to center

    stick.style.left =
        "80px";


    stick.style.top =
        "80px";


    // STOP MOTORS

    sendMotors(
        0,
        0
    );

}}


// ============================================================
// POINTER DOWN
// ============================================================

base.addEventListener(
    "pointerdown",

    function(event) {{

        active = true;


        base.setPointerCapture(
            event.pointerId
        );


        const rect =
            base.getBoundingClientRect();


        control(

            event.clientX -
            rect.left -
            center,

            event.clientY -
            rect.top -
            center

        );

    }}

);


// ============================================================
// POINTER MOVE
// ============================================================

base.addEventListener(
    "pointermove",

    function(event) {{

        if (!active) {

            return;

        }


        const rect =
            base.getBoundingClientRect();


        control(

            event.clientX -
            rect.left -
            center,

            event.clientY -
            rect.top -
            center

        );

    }}

);


// ============================================================
// POINTER UP
// ============================================================

base.addEventListener(
    "pointerup",

    function() {{

        release();

    }}

);


// ============================================================
// POINTER CANCEL
// ============================================================

base.addEventListener(
    "pointercancel",

    function() {{

        release();

    }}

);


</script>


</body>

</html>
"""


st.iframe(
    joystick_html,
    height=350
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
# MANUAL CONNECTION TEST
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
                "Wemos returned an error."
            )


    except requests.RequestException as error:

        st.error(
            f"Connection failed: {error}"
        )
