import streamlit as st
import streamlit.components.v1 as components
import requests
import time

# ============================================================
# CONFIG
# ============================================================

WEMOS_IP = "192.168.1.100"   # <-- CHANGE THIS
WEMOS_URL = f"http://{WEMOS_IP}"

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SUBMARINE V2",
    page_icon="⚓",
    layout="wide",
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
    font-size: 2.4rem;
}

.status {
    text-align: center;
    font-size: 1.1rem;
    margin-bottom: 15px;
}

.camera {
    background: #111820;
    border: 2px solid #263241;
    border-radius: 15px;
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #8793a3;
    font-size: 1.2rem;
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
# WEMOS CONNECTION TEST
# ============================================================

def wemos_request(endpoint):

    try:
        response = requests.get(
            f"{WEMOS_URL}{endpoint}",
            timeout=0.5
        )

        return response.text

    except requests.RequestException:
        return None


# ============================================================
# CAMERA PLACEHOLDER
# ============================================================

st.markdown(
    """
    <div class="camera">
        📹 PHONE REAR CAMERA<br>
        <small>Camera integration coming next</small>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# SPEED
# ============================================================

st.subheader("🎚️ MOTOR SPEED")

speed = st.slider(
    "Speed",
    min_value=0,
    max_value=100,
    value=30,
    step=1,
    label_visibility="collapsed"
)

st.markdown(
    f"<h2 style='text-align:center'>{speed}%</h2>",
    unsafe_allow_html=True
)


# ============================================================
# JOYSTICK
# ============================================================

st.subheader("🕹️ CONTROL")

joystick_html = """

<!DOCTYPE html>

<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<style>

body {

    margin: 0;

    background: transparent;

    display: flex;

    justify-content: center;

    align-items: center;

    height: 300px;

    overflow: hidden;

}

#joystick {

    width: 220px;

    height: 220px;

    border-radius: 50%;

    background: #202833;

    border: 3px solid #394654;

    position: relative;

    touch-action: none;

}

#stick {

    width: 75px;

    height: 75px;

    border-radius: 50%;

    background: #4b83ff;

    position: absolute;

    left: 72px;

    top: 72px;

    box-shadow: 0 0 20px rgba(75,131,255,0.5);

}

</style>

</head>


<body>


<div id="joystick">

    <div id="stick"></div>

</div>


<script>


const joystick =
    document.getElementById("joystick");

const stick =
    document.getElementById("stick");


const center = 110;

const maxDistance = 75;


let active = false;


function moveStick(clientX, clientY) {

    const rect =
        joystick.getBoundingClientRect();


    let x =
        clientX - rect.left - center;

    let y =
        clientY - rect.top - center;


    const distance =
        Math.sqrt(x*x + y*y);


    if (distance > maxDistance) {

        x =
            x / distance * maxDistance;

        y =
            y / distance * maxDistance;

    }


    stick.style.left =
        (center + x - 37.5) + "px";


    stick.style.top =
        (center + y - 37.5) + "px";


    let command = "STOP";


    const deadzone = 20;


    if (Math.abs(x) < deadzone &&
        Math.abs(y) < deadzone) {

        command = "STOP";

    }

    else if (Math.abs(y) > Math.abs(x)) {

        if (y < 0) {

            command = "FORWARD";

        } else {

            command = "BACK";

        }

    }

    else {

        if (x < 0) {

            command = "LEFT";

        } else {

            command = "RIGHT";

        }

    }


    window.parent.postMessage({

        type: "SUB_COMMAND",

        command: command

    }, "*");

}


function releaseStick() {

    active = false;


    stick.style.left =
        "72px";

    stick.style.top =
        "72px";


    window.parent.postMessage({

        type: "SUB_COMMAND",

        command: "STOP"

    }, "*");

}


joystick.addEventListener(

    "pointerdown",

    function(event) {

        active = true;

        joystick.setPointerCapture(
            event.pointerId
        );

        moveStick(
            event.clientX,
            event.clientY
        );

    }

);


joystick.addEventListener(

    "pointermove",

    function(event) {

        if (!active) return;

        moveStick(
            event.clientX,
            event.clientY
        );

    }

);


joystick.addEventListener(

    "pointerup",

    releaseStick

);


joystick.addEventListener(

    "pointercancel",

    releaseStick

);


</script>


</body>

</html>

"""


components.html(
    joystick_html,
    height=320
)


# ============================================================
# COMMAND BUTTONS
# ============================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "⬅ LEFT",
        use_container_width=True
    ):

        wemos_request(
            f"/cmd?move=LEFT"
        )


with col2:

    if st.button(
        "🛑 EMERGENCY STOP",
        use_container_width=True
    ):

        wemos_request(
            "/cmd?move=STOP"
        )


with col3:

    if st.button(
        "RIGHT ➡",
        use_container_width=True
    ):

        wemos_request(
            "/cmd?move=RIGHT"
        )


# ============================================================
# SPEED CONTROL
# ============================================================

# Streamlit slider sends the speed to the Wemos.

if st.button(
    f"⚙️ APPLY SPEED {speed}%",
    use_container_width=True
):

    result = wemos_request(
        f"/speed?value={speed}"
    )

    if result:

        st.success(
            f"Motor speed set to {speed}%"
        )

    else:

        st.error(
            "❌ Wemos not reachable"
        )


# ============================================================
# CONNECTION
# ============================================================

st.divider()

if st.button(
    "📡 TEST WEMOS CONNECTION",
    use_container_width=True
):

    result = wemos_request(
        "/"
    )

    if result:

        st.success(
            "🟢 WEMOS ONLINE"
        )

    else:

        st.error(
            "🔴 WEMOS OFFLINE"
        )
