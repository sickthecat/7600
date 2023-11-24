import serial
import time

# ASCII art of a cell phone tower //replaced with a fucking cat because i could not find a decent cell tower ascii art.
cat_moon = r"""

         *                  *
             __                *
          ,db'    *     *
         ,d8/       *        *    *
         888
         `db\       *     *
           `o`_                    **
      *               *   *    _      *
            *                 / )
         *    (\__/) *       ( (  *
       ,-.,-.,)    (.,-.,-.,-.) ).,-.,-.
      | @|  ={      }= | @|  / / | @|o |
     _j__j__j_)     `-------/ /__j__j__j_
     ________(               /___________
      |  | @| \              || o|O | @|
      |o |  |,'\       ,   ,'"|  |  |  |  hjw
     vV\|/vV|`-'\  ,---\   | \Vv\hjwVv\//v
                _) )    `. \ /
               (__/       ) )
                         (_/


"""

def send_at_command(port, command):
    """
    Send an AT command to the modem and return the response.
    """
    try:
        with serial.Serial(port, 115200, timeout=1) as ser:
            ser.write((command + '\r\n').encode())
            time.sleep(1)
            response = ser.read_all()
            return response.decode().strip()
    except Exception as e:
        return f"Error: {e}"

def make_call(port, phone_number):
    """
    Make a phone call to the specified phone number using the modem on the given COM port.
    """
    try:
        with serial.Serial(port, 115200, timeout=1) as ser:
            ser.write(f'ATD{phone_number};\r\n'.encode())  # Dial command
            time.sleep(5)  # Wait for the call to be established
            response = ser.read_all()
            return "Call initiated" if b'OK' in response else "Failed to initiate call"
    except Exception as e:
        return f"Error: {e}"

def send_sms(port, phone_number, message):
    """
    Send an SMS message to the specified phone number using the modem on the given COM port.
    """
    try:
        with serial.Serial(port, 115200, timeout=1) as ser:
            ser.write(b'AT+CMGF=1\r\n')  # Set modem to SMS text mode
            time.sleep(1)
            ser.write(f'AT+CMGS="{phone_number}"\r\n'.encode())  # Set recipient phone number
            time.sleep(1)
            ser.write((message + '\x1a').encode())  # Message content and CTRL+Z (end of message)
            time.sleep(5)
            response = ser.read_all()
            return "SMS sent successfully" if b'+CMGS' in response else "Failed to send SMS"
    except Exception as e:
        return f"Error: {e}"

def main():
    # Display ASCII art and text
    print(cat_moon)
    print("Waveshare SIM7600G-H AT Commands script by _SiCk")
    print("https://afflicted.sh")

    modem_port = input("Enter the COM port of the modem (e.g., COM3): ")

    while True:
        print("\nOptions:")
        print("1. Make a Call")
        print("2. Request Manufacturer Identification")
        print("3. Request Model Identification")
        print("4. Request Product Serial Number Identification")
        print("5. Request Module Version and Chip")
        print("6. Request SIM Card State")
        print("7. Read ICCID from SIM Card")
        print("8. Request Subscriber Number")
        print("9. Preferred Mode Selection")
        print("10. Check Current Network Operator")
        print("11. Send SMS")
        print("12. Exit")

        choice = input("Enter your choice (1-12): ")

        if choice == '1':
            phone_number = input("Enter the phone number to call: ")
            call_response = make_call(modem_port, phone_number)
            print(call_response)
        elif choice == '2':
            manufacturer_response = send_at_command(modem_port, 'AT+CGMI')
            print(manufacturer_response)
        elif choice == '3':
            model_response = send_at_command(modem_port, 'AT+CGMM')
            print(model_response)
        elif choice == '4':
            serial_number_response = send_at_command(modem_port, 'AT+CGSN')
            print(serial_number_response)
        elif choice == '5':
            module_info_response = send_at_command(modem_port, 'AT+CSUB')
            print(module_info_response)
        elif choice == '6':
            sim_card_state_response = send_at_command(modem_port, 'AT+CPIN?')
            print(sim_card_state_response)
        elif choice == '7':
            iccid_response = send_at_command(modem_port, 'AT+CICCID')
            print(iccid_response)
        elif choice == '8':
            subscriber_number_response = send_at_command(modem_port, 'AT+CNUM')
            print(subscriber_number_response)
        elif choice == '9':
            preferred_mode_response = send_at_command(modem_port, 'AT+CNMP?')
            print(preferred_mode_response)
        elif choice == '10':
            current_operator_response = send_at_command(modem_port, 'AT+COPS?')
            print(current_operator_response)
        elif choice == '11':
            phone_number = input("Enter the phone number to send the SMS to: ")
            message = input("Enter the SMS message: ")
            sms_response = send_sms(modem_port, phone_number, message)
            print(sms_response)
        elif choice == '12':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
