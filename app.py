from flask import Flask, render_template, request, redirect, url_for, session
import subprocess, os
import re

# ANSI escape sequence regex pattern
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
# Initialize the Flask application
app = Flask(__name__)
# Generate a random secret key for session management
app.secret_key = os.urandom(24)

def run_cli_tool(check_choice, choice, address, extra_choices=[]):
    """
    Executes the CLI tool with the specified choice, address, and any additional arguments.
    """
    # Mapping of web interface choices to their corresponding CLI command identifiers
    choice_map = {
        "ip_finder": "1",
        "port_scanner": "2",
        "wayback_urls": "3",
        "subdomain_listing": "4",
        "get_robots": "5",
        "host_info_scanner": "6",
        "dns_lookup": "7",
        "hosts_search": "8",
        "geo_location": "9",
        "host_information": "10",
        "list_shared_dns_servers": "11",
        "dorking": "12",
        "Check_if_domain_email_spoofable": "13",
        "dos_attack": "14"       
    }
    # Initialize the command with the python interpreter, script name, and basic arguments
    command = ['python3', 'webinfofinder.py']    
    # Combine basic command with choice and additional options
    input_arguments = [check_choice, choice_map[choice], address] + extra_choices
    # Execute the CLI tool in a subprocess
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )    
    
    try:
        # Send the arguments to the CLI tool, handling each argument individually
        for argument in input_arguments:
            process.stdin.write(argument + '\n')
            process.stdin.flush()       
        # Signal the end of input to the CLI tool
        process.stdin.close()
        # Read the output and error streams
        output = process.stdout.read()
        error = process.stderr.read()

        print('DEBUG OUTPUT:', output)  # Debugging line
        print('DEBUG ERROR:', error)    # Debugging line

        # Wait for the subprocess to terminate
        process.wait()
        # Decode output and remove ANSI escape characters.
        output = ansi_escape.sub('', output)        
        if process.returncode != 0:
            # Return error message if the subprocess didn't exit cleanly
            print('DEBUG ERROR WITH NON-ZERO EXIT CODE:', error)  # Debugging line
            return f"Error: {error.strip()}"
        return output.strip()
    except KeyError:
        # Handle incorrect choice inputs
        return "Invalid choice. Please check the choice mapping."
    except Exception as e:
        print('DEBUG EXCEPTION:', e)  # Debugging line
        # Catch all other errors
        return f"Unexpected error: {str(e)}"


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    The home route that handles the landing page and form submission.
    """
    # Initial landing page which displays the form
    if request.method == 'POST':
        # Store the address provided by the user in the session
        session['address'] = request.form['address']
        session['check_choice'] = request.form['check_choice']
        # Redirect to the choice page after form submission
        return redirect(url_for('choice'))
    # Render the welcome page
    return render_template('welcome.html')

@app.route('/choice', methods=['GET', 'POST'])
def choice():
    """
    A route that presents the user with different action choices after the initial address input.
    """
    # Retrieve address and check choice from session for a GET request or set default
    address = session.get('address', '')
    check_choice = session.get('check_choice', '')

    if request.method == 'POST':
        # Capture the user's choice and store it in the session
        choice_type = request.form.get('choice_type')
        check_choice = session['check_choice']
        session['choice_type'] = choice_type
        # Redirect to specific routes for actions requiring further input
        if choice_type in ['wayback_urls', 'port_scanner', 'dorking', 'dos_attack']:
            # Redirect to the specific route for further input from the user
            return redirect(url_for(choice_type))
        # Directly execute the CLI tool for actions not requiring additional input
        result = run_cli_tool(check_choice, choice_type, address)
        return render_template('result.html', result=result)
    # Render the choice selection page
    return render_template('choice.html', address=address)

@app.route('/port_scanner', methods=['GET', 'POST'])
def port_scanner():
    if request.method == 'POST':
        # Capture the user's choice and store it in the session
        port_choice = request.form.get('port_choice')
        port_number = request.form.get('port_number', None)
        address = session.get('address')
        choice_type = session.get('choice_type')
        check_choice = session.get('check_choice')
        # Capture additional input required for their specific action
        extra_choices = []
        if port_choice == 'single_port' and port_number:
            extra_choices += ['1', port_number]
        elif port_choice == 'all_ports':
            extra_choices.append('2')
        # Execute the CLI tool for actions with requiring additional input
        result = run_cli_tool(check_choice, choice_type, address, extra_choices)
        # Render the result page
        return render_template('result.html', result=result)
    # Render the port scanner page
    return render_template('port_scanner.html')
            
@app.route('/wayback_urls', methods=['GET', 'POST'])
def wayback_urls():
    if request.method == 'POST':
    # Capture the choice from the form
        status_code_choice = request.form.get('wayback_urls_choice')
        address = session.get('address')
        choice_type = session.get('choice_type')   
        check_choice = session.get('check_choice')
    # Map the status_code_choice to the actual CLI expected input
        status_code_map = {
        "status_code_200": "1",
        "status_code_302": "2",
        "status_code_403": "3",
        "status_code_404": "4",
        "all_urls": "5"
        }
        # Execute the CLI tool for actions with requiring additional input
        result = run_cli_tool(check_choice, choice_type, address, [status_code_map[status_code_choice]])
        pass
        # Render the result page
        return render_template('result.html', result=result)
    # Render the wayback urls page
    return render_template('wayback_urls.html')

@app.route('/dorking', methods=['GET', 'POST'])
def dorking():
    if request.method == 'POST':
        # Call the CLI tool with the keywords
        keywords = request.form.get('keywords') 
        # Capture the user's choice and store it in the session
        address = session.get('address')
        choice_type = session.get('choice_type')
        check_choice = session.get('check_choice')
        # Execute the CLI tool for actions with requiring additional input
        result = run_cli_tool(check_choice, choice_type, address, [keywords])
        pass
        # Render the result page
        return render_template('result.html', result=result)
    # Render the dorking page
    return render_template('dorking.html')

@app.route('/dos_attack', methods=['GET', 'POST'])
def dos_attack():
    if request.method == 'POST':
        # Call the CLI tool with the keywords
        attack_argument = request.form.get('attack_argument') 
        # Capture the user's choice and store it in the session
        address = session.get('address')
        choice_type = session.get('choice_type')
        check_choice = session.get('check_choice')
        # Execute the CLI tool for actions with requiring additional input
        result = run_cli_tool(check_choice, choice_type, address, [attack_argument])
        pass
        # Render the result page
        return render_template('result.html', result=result)
    # Render the dorking page
    return render_template('dos_attack.html')

if __name__ == '__main__':
    # Start the Flask application
    app.run(debug=True)