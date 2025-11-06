#include <Arduino.h>
#include <USBKeyboard.h>

USBKeyboard key;

/*
 * Check for local commits that need to be pushed
 * Check origin for commit pulls
 * Check for code that has not been committed
 */
void githubAnalyzation()
{
}

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

/*
 * Ctrl + B - Opens bookmark menu
 */
void openBookmarkFolder(int bookmarkItem)
{
    // do this later!
}

String query(const char *prompt)
{
    key.key_code('t', 0x05); // terminal shortcut
    delay(750);
    key.printf("bash -c 'clear;echo ");
    key.printf(prompt);
    key.printf("; read r; echo $r > /dev/ttyACM*'\n"); // script to collect user feedback

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

    delay(200);
    key.printf("exit\n"); // close terminal window
    delay(200);

    return response;
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
    String response = query("Enter subworkflow? [minecraft], [research], [other] ... 5s");

    openApplication("firefox");
    if (response.equals("minecraft") || response.equals("java"))
    {
        openBookmarkFolder(4);
    }
    else if (response.equals("research") || response.equals("uni"))
    {
        openBookmarkFolder(3);
    }

    openApplication("intellij");
    openApplication("github desktop");
    githubAnalyzation();
}

/*
 * Retrieve stored workflow state (store via enum)
 */
void setup()
{
    Serial.begin(9600);
    // method testing code
    delay(1000);
    programmingWorkflow();
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

void loop()
{
}