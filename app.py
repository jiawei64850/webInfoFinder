from flask import Flask, render_template, request, redirect, url_for, session, flash
import subprocess, os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random key


def run_cli_tool(address, choice_type, port_choice=None, port_number=None, wayback_urls_choice=None):
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

    # Prepare the command and the arguments to be sent to the CLI tool
    command = ['python3', 'webinfofinder.py']
    

    input_arguments = [address, choice_map[choice]]

    # Include additional arguments based on user's choice
    if choice_type == 'port_scanner':
        if port_choice == 'single_port' and port_number:
            input_arguments.extend(['1', port_number])
        elif port_choice == 'all_ports':
            input_arguments.append('2')
    
    if choice_type == 'wayback_urls':
        if wayback_urls_choice == "status_code_200":
            input_arguments.append('1')
        elif wayback_urls_choice == "status_code_302":
            input_arguments.append('2')
        elif wayback_urls_choice == "status_code_303":
            input_arguments.append('3')
        elif wayback_urls_choice == "status_code_404":
            input_arguments.append('4')
        else:
            input_arguments.append('5')


    if choice_type == 'dorking':
        input_arguments.extend('keywords')


    # Start the CLI tool process
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


    try:
        # Send the arguments to the CLI tool, line by line
        for argument in input_arguments:
            process.stdin.write(argument + '\n')
            process.stdin.flush()
        
        # Close stdin to signal to the CLI tool that input is complete
        process.stdin.close()

        # Wait for the process to complete and capture output
        output = process.stdout.read()
        error = process.stderr.read()
        
        # Wait for process 
        process.wait()
        
        if process.returncode != 0:
            # Handle error accordingly
            return f"Error: {error}"

        return "CLI Output:", output

    except KeyError:
        return "Invalid choice. Please check the choice mapping."
    except Exception as e:
        return f"Unexpected error: {str(e)}"






@app.route('/', methods=['GET', 'POST'])
def home():
    # Initial landing page which displays the form
    if request.method == 'POST':
        # Process the form data and redirect
        session['address'] = request.form['address']
        return redirect(url_for(address=session['address']))
    return render_template('welcome.html')


@app.route('/choice', methods=['GET', 'POST'])
def choice():
    # Retrieve address from session for a GET request or set default
    address = session.get('address', '')

    if request.method == 'POST':
        choice_type = request.form.get('choice_type')
        # ... your POST handling logic ...
        return redirect(url_for('perform_action', choice_type=choice_type))
    # Retrieve address from session for a GET request or set default
    address = session.get('address', '')
    choice_type = request.args.get('choice_type', '')  # This will get the choice_type query parameter if present

    return render_template('choice.html', address=address)

@app.route('/perform_action', methods=['GET', 'POST'], strict_slashes=False)

def perform_action():
    # Retrieve 'address' from the session
    address = session.get('address')
    choice_type = request.form.get('choice_type')
    
   #if not address:
        # Handle the error, e.g., by flashing a message or redirecting to home
        #flash('No address found. Please enter an address.')
        #return redirect(url_for('home'))

    # Check if the choice requires additional options
    if choice_type in ['wayback_urls', 'port_scanner', 'dorking']:
        # Redirect to the specific route for further input from the user
        return redirect(url_for(choice_type))
    
    # For choices that do not require additional options, run the CLI tool
    result = run_cli_tool(address, choice_type)
    return render_template('result.html', result=result)

@app.route('/port_scanner', methods=['POST'])
def port_scanner():
    port_choice = request.form.get('port_choice')
    address = session.get('address')
    
    if port_choice == 'single_port':
        port_number = request.form.get('port_number')
        if not port_number:
            return render_template('port_scanner.html', error="Please enter a port number.")
        result = run_cli_tool('port_scanner', address, port_choice, port_number)
    
    elif port_choice == 'all_ports':
        result = run_cli_tool('port_scanner', address, port_choice)

    else:
        return render_template('port_scanner.html', error="Invalid port choice selected.")

    return render_template('result.html', result=result)




@app.route('/wayback_urls', methods=['POST'])
def wayback_urls():
    if request.method == 'POST':
    # Capture the choice from the form
        status_code_choice = request.form.get('status_code_choice')
    
    # Map the status_code_choice to the actual CLI expected input
        status_code_map = {
        "status_code_200": "1",
        "status_code_302": "2",
        "status_code_403": "3",
        "status_code_404": "4",
        "all_urls": "5"
        }
    
    # Use the session or a hidden input field to retrieve the 'address'
        address = session.get('address')  # Assuming you have stored the address in the session earlier

    # Call the CLI tool with the mapped status code and the address
        result = run_cli_tool('wayback_urls', address, [status_code_map[status_code_choice]])
        pass

    # Render the result page
    return render_template('result.html', result=result)


@app.route('/dorking', methods=['POST'])
def dorking():
    if request.method == 'POST':
        # Call the CLI tool with the keywords
        keywords = request.form.get('keywords') 
        address = session.get('address')
        result = run_cli_tool('dorking', session.get('address'), [keywords])
        pass
        # Render the result page
        return render_template('result.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)






