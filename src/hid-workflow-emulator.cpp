#include <Arduino.h>
#include <USBKeyboard.h>

USBKeyboard key;

/*
 * Loops through each character and types it
 */
void typeAnimation(String s)
{
    for (unsigned int i = 0; i < s.length(); i++)
    {
        key.key_code(s.charAt(i));
        delay(50);
    }
    delay(50);
}

/*
 * Opens up application menu and selects respective application
 */
void openApplication(String s)
{
    key.key_code(0, 0x08); // super
    delay(100);
    typeAnimation(s);
    key.key_code_raw(0x28); // enter
}

String query(String prompt)
{
    key.key_code('t', 0x05); // terminal shortcut
    delay(750);
    // key.printf("chmod 666 /dev/ttyACM0\n"); // allows communication to usb
    delay(5000);
    key.printf("bash -c 'echo Reading input for next 5 seconds...; read r; echo $r > /dev/ttyACM0'\n"); // script to collect user feedback

    delay(1000);

    String response = "";
    unsigned long timeout = millis() + 5000;

    while (millis() < timeout)
    {
        if (Serial.available())
        {
            String line = Serial.readStringUntil('\n');
            if (line.length() > 0)
            {
                response = line;
                break;
            }
        }
    }

    delay(500);

    typeAnimation("Logged: " + response);
}

/*
 * Retrieve stored workflow state (store via enum)
 */
void setup()
{
    Serial.begin(9600);
    // method testing code
    delay(1000);
    query("blank");
}

/*
 * Check if on Linux: change boot order
 * Check if on Windows: change boot order
 * Restart machine
 */
void dualBootWorkflow()
{
}

/*
 * Query programming subject
 *    Minecraft / Java development: Pull up documentation
 *    Research: Pull up specific documentation & Canvas login
 *    Other: Proceed
 *
 * Open Firefox in programming profile
 * Open Intellij
 *
 * Open GitHub Desktop
 * Run GitHub analyzation script
 */
void programmingWorkflow()
{
}

/*
 * Open platformIO folder
 * Open KiCAD
 */
void circuitsWorkflow()
{
}

/*
 * Start backup processes
 */
void systemAdminWorkflow()
{
}

/*
 * Check for local commits that need to be pushed
 * Check origin for commit pulls
 * Check for code that has not been committed
 */
void githubAnalyzation()
{
}

void loop()
{
}