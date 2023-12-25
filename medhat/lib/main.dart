// ignore_for_file: deprecated_member_use
import 'dart:convert';
import 'registration_service.dart';
import 'package:flutter/material.dart';
import 'package:line_icons/line_icons.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:google_nav_bar/google_nav_bar.dart';
import 'api_service2.dart';
import 'login_service.dart';
import 'retrieve_service.dart';

final TextEditingController usernameController = TextEditingController();
final TextEditingController passwordController = TextEditingController();
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Medhat',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color.fromARGB(255, 3, 25, 60)),
        useMaterial3: true,
      ),
      home: const HomePage(title: 'Main Menu'),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({Key? key, required this.title}) : super(key: key);
  final String title;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
      ),
      body: Center( // Wrapping Column with Center
        child: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
             Image.asset(
                  'assets/hi-robot.gif', // Replace with your image
                  width: 275, // Adjust width as needed
                  height: 275, // Adjust height as needed
                  fit: BoxFit.cover,
                ),
              Image.asset(
                  'assets/medhat_logo.png', // Replace with your image
                  width: 300, // Adjust width as needed
                  height: 90, // Adjust height as needed
                  fit: BoxFit.cover,
                ),  
            const SizedBox(height: 16),
              OutlinedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) =>  LoginPage()),
                  );
                },
              child: const Text('Log In',style:TextStyle(color: Color.fromARGB(255, 1, 60, 120))),
              ),
              const SizedBox(height: 16),
              OutlinedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const CreateAccountPage(title: 'Create your Account')),
                  );
                },
              child: const Text('Create a new account',style:TextStyle(color: Color.fromARGB(255, 1, 60, 120))),
              )
          ],
        ),
        ),
      ),
    );
  }
}

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}
class _LoginPageState extends State<LoginPage> {
  
  bool loginSuccessful = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromARGB(255, 1, 60, 120),
        title: Text('Log In',style: TextStyle(color: Color.fromARGB(255, 254, 254, 254))),

      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: usernameController,
              decoration: InputDecoration(labelText: 'Username',labelStyle: TextStyle(color: Color.fromARGB(255, 1, 60, 120))),
            ),
            TextField(
              controller: passwordController,
              decoration: InputDecoration(labelText: 'Password',labelStyle: TextStyle(color: Color.fromARGB(255, 1, 60, 120))),
              obscureText: true,
            ),
            SizedBox(height: 16),

            if (!loginSuccessful)
              Text(
                'Login unsuccessful. Please check your credentials.',
                style: TextStyle(color: Colors.red),
              ),
            ElevatedButton(
              onPressed: () async {
                try {
                  final LoginService loginService = LoginService('http://192.168.37.108:5000');
                  String message = await loginService.loginUser(
                    username: usernameController.text,
                    password: passwordController.text,
                  );

                  // Handle the login success or failure here
                  print('Login success: $message');
                  if (message == "Login successful") {
                    Navigator.push(context,
                        MaterialPageRoute(builder: (context) => OptionPage()));
                    setState(() {
                      // Set loginSuccessful to true to hide the red line
                      loginSuccessful = true;
                    });
                  } else {
                    setState(() {
                      // Set loginSuccessful to false to show the red line
                      loginSuccessful = false;
                    });
                  }
                } catch (e) {
                  print('Error during login: $e');
                }
              
              },
              child: Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
}
    


class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final ApiService apiService = ApiService('http://192.168.37.108:5000');
  final TextEditingController userInputController = TextEditingController();
  final List<String> chatHistory = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Chatbot App'),
      ),
      body: Column(
        children: [
          Expanded(
            child:ListView.builder(
  itemCount: chatHistory.length,
  itemBuilder: (context, index) {
    final isUserMessage = index % 2 == 0; // Alternate between user and bot messages for demonstration
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Align(
        alignment: isUserMessage ? Alignment.topRight : Alignment.topLeft,
        child: Container(
          padding: EdgeInsets.all(8.0),
          decoration: BoxDecoration(
            color: isUserMessage ? Color.fromARGB(255, 33, 72, 243) : Color.fromARGB(255, 193, 211, 255),
            borderRadius: BorderRadius.circular(12.0),
          ),
          child: Text(
            chatHistory[index],
            style: TextStyle(
              color: isUserMessage ? Colors.white : Colors.black,
            ),
          ),
        ),
      ),
    );
  },
),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: userInputController,
                    decoration: InputDecoration(hintText: 'Type your message...'),
                  ),
                ),
                ElevatedButton(
                  onPressed: () => sendMessage(),
                  child: Text('Send'),
                ),
              ],
            ),
          ),
        ],
      ),
      bottomNavigationBar: 
      GNav(
        rippleColor: const Color.fromARGB(255, 129, 122, 122), // tab button ripple color when pressed
      hoverColor: Color.fromARGB(255, 240, 236, 236), // tab button hover color
       haptic: true, // haptic feedback
      tabBorderRadius: 30, 
    tabActiveBorder: Border.all(color: Colors.black, width: 1.5), // tab button border
    tabBorder: Border.all(color: Color.fromARGB(255, 191, 217, 246), width: 1), // tab button border
    tabShadow: [BoxShadow(color: Color.fromARGB(255, 191, 217, 246).withOpacity(0.5), blurRadius: 8)], // tab button shadow
    curve: Curves.easeOutExpo, // tab animation curves
    duration: Duration(milliseconds: 900), // tab animation duration
    gap: 8, // the tab button gap between icon and text 
    color: Color.fromARGB(255, 1, 75, 118), // unselected icon color
    activeColor: Color.fromARGB(255, 98, 163, 233), // selected icon and text color
    iconSize: 35, // tab button icon size
    tabBackgroundColor: Color.fromARGB(255, 191, 217, 246).withOpacity(0.1), // selected tab background color
    padding: EdgeInsets.symmetric(horizontal: 10, vertical: 5), // navigation bar padding
    tabs: [
      GButton(
      icon: LineIcons.robot,
      text: 'Chat with Medhat'
      ),
      GButton(
      icon: LineIcons.newspaper,
      text: 'News',
      onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) =>  const FurtherInfoPage(title: 'FurtherInfoPage'))
                  );
                }
      ),
      GButton(
      icon: LineIcons.user,
      text: 'Profile',
      onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) =>  OptionPage())
                  );
                }
      )
      
  ]
      ),    
    
    );
  }

  Future<void> sendMessage() async {
    String userMessage = userInputController.text;
    setState(() {
      chatHistory.add('You: $userMessage');
      userInputController.clear();
    });

    try {
      // Replace the following line with the actual call to your chatbot API
      String chatbotResponse = await apiService.chatWithBot(userMessage);
      setState(() {
        chatHistory.add('Medhat: $chatbotResponse');
      });
    } catch (e) {
      print('Error communicating with the chatbot: $e');
      setState(() {
        chatHistory.add('Error communicating with the chatbot');
      });
    }
  }
}


class CreateAccountPage extends StatefulWidget {
  const CreateAccountPage({Key? key, required this.title}) : super(key: key);
  final String title;

  @override
  _CreateAccountPageState createState() => _CreateAccountPageState();
}
class _CreateAccountPageState extends State<CreateAccountPage> {
  final TextEditingController nameController = TextEditingController();
  final TextEditingController userController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  String selectedDate = '';
  String genderValue = '';
  final TextEditingController chronicController = TextEditingController();

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(1920),
      lastDate: DateTime(2024),
    );

    if (picked != null && picked != DateTime.now()) {
      setState(() {
        selectedDate = DateTime(picked.year, picked.month, picked.day).toString();
      });
    }
  }

  String? validatePassword(String? value) {
    if (value == null || value.isEmpty) {
      return 'Password is required';
    } else if (value.length < 8 || value.length > 20) {
      return 'Password must be between 8 and 20 characters';
    }
    return null;
  }
  String? validateName(String? value) {
    if (value == null || value.isEmpty) {
      return 'Name is required';
    } else if (value.length < 2 || value.length > 100 || !RegExp(r'^[a-zA-Z]+$').hasMatch(value)) {
      return 'Invalid name';
    }
    return null;
  }

 ///////// ADD UNAME VALIDATION FUNC
  String? validateUName(String? value) {
    if (value == null || value.isEmpty) {
      return 'User name is required';
    } else if (value.isEmpty || value.length > 100) {
      return 'Invalid name';
    }
    return null;
  }

  String? validateDOB(String? value) {
    if (value == null || value.isEmpty) {
      return 'Date of birth is required';
    }
    // Add additional date validation if needed
    return null;
  }

  String? validateGender(String? value) {
    if (value == null || value.isEmpty) {
      return 'Gender is required';
    }
    return null;
  }

  String? validateChronicIllness(String? value) {
    if (value == null || value.isEmpty) {
      return 'Chronic Illness is required';
    } else if (value.length < 2 || value.length > 100 || !RegExp(r'^[a-zA-Z]+$').hasMatch(value)) {
      return 'Invalid chronic illness';
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromARGB(255, 1, 60, 120),
        title: Text(widget.title,style:TextStyle(color: Color.fromARGB(255, 254, 254, 254))),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(10.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Name',style:TextStyle(color: Color.fromARGB(255, 1, 60, 120))),
              const SizedBox(height: 8),
              TextFormField(
                controller: nameController,
                validator: validateName,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'Type here...',
                ),
              ),
              const Text('User name',style:TextStyle(color: Color.fromARGB(255, 1, 60, 120))),
              const SizedBox(height: 8),
              TextFormField(
                controller: userController,
                validator: validateUName, // ADD VALIDATOR <<<<<
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'Type here...',
                ),
              ),
              const Text('Password',style:TextStyle(color: Color.fromARGB(255, 1, 60, 120))),
              const SizedBox(height: 8),
              TextFormField(
                controller: passwordController,
                validator: validatePassword,
                obscureText: true,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'Type here...',
                ),
              ),
              const Text('Date of birth',style:TextStyle(color: Color.fromARGB(255, 1, 60, 120))),
              InkWell(
                onTap: () {
                  _selectDate(context);
                },
                child: InputDecorator(
                  decoration: InputDecoration(
                    labelText: '',
                    hintText: 'Select Date',
                    // You can customize the appearance further
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: <Widget>[
                      Text(selectedDate),
                      Icon(Icons.calendar_today),
                    ],
                  ),
                ),
              ),
              const Text('Gender',style:TextStyle(color: Color.fromARGB(255, 1, 60, 120))),
              Row(
                children: <Widget>[
                  Radio<String>(
                    value: 'M',
                    groupValue: genderValue, // You need to declare a variable to hold the selected value
                    onChanged: (String? value) {
                      setState(() {
                        genderValue = value!;
                      });
                    },
                  ),
                  const Text('Male'),
                  Radio<String>(
                    value: 'F',
                    groupValue: genderValue,
                    onChanged: (String? value) {
                      setState(() {
                        genderValue = value!;
                      });
                    },
                  ),
                  const Text('Female'),
                ],
              ),
              const Text('Chronic Illness',style:TextStyle(color: Color.fromARGB(255, 1, 60, 120))),
              const SizedBox(height: 8),
              TextFormField(
                controller: chronicController,
                validator: validateChronicIllness,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'Type here...',
                ),
              ),
              const SizedBox(height: 16),
              Center(
                child: ElevatedButton(
                  onPressed: () async {
                    print("HERE!");
                    //if (Form.of(context)!.validate()) {
                      // Validation passed, proceed with registration
                      try {
                        final RegService registrationService = RegService('http://192.168.37.108:5000');
                        String message = await registrationService.registerUser(
                          password: passwordController.text,
                          name: nameController.text,
                          date_of_birth: selectedDate,
                          gender: genderValue,
                          chronic_illness: chronicController.text,
                          username: userController.text,
                        );
                        print('Registration success: $message');
                      } catch (e) {
                        print(passwordController.text);
                        print(nameController.text);
                        print(selectedDate);
                        print(genderValue);
                        print(chronicController.text);
                        print(userController.text);
                        print('Error during registration: $e');
                      }
                    
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) =>  OptionPage())
                  );  
                  },
                  child: const Text('Create account',style:TextStyle(color: Color.fromARGB(255, 1, 60, 120))),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class OptionPage extends StatefulWidget {
  const OptionPage({Key? key}) : super(key: key);
 
  @override
  State<OptionPage> createState() => _OptionPageState();
}
  
 class _OptionPageState extends State<OptionPage> {
  String uname = usernameController.text;
  late String name = "";
  late String dateOfBirth = "dob";
  late String gender = "gender";
  late String chronicIllness = "chronic";
  late String prevDiag = "last";
  late Map<String, dynamic> userInfo;

  Future<void> _retrieveUserInfo() async {
    try {
      final RetrieveService retrieveService = RetrieveService('http://192.168.37.108:5000');  // Update this URL
      userInfo = await retrieveService.retrieveUserInfo(
        username: usernameController.text,
      );

      // Handle user information as needed
      setState(() {
        name = userInfo['name'];
        dateOfBirth = userInfo['date_of_birth'];
        gender = userInfo['gender'];
        chronicIllness = userInfo['chronic_illness'];
        prevDiag = userInfo['diag'];
      });

      // Do something with the retrieved information
      print('Name: $name');
      print('Date of Birth: $dateOfBirth');
      print('Gender: $gender');
      print('Chronic Illness: $chronicIllness');
      print('Previous Diagnoses: $prevDiag');

    } catch (e) {
      print('Error retrieving user information: $e');
    }
  }
  @override
  void initState() {
    super.initState();
    _retrieveUserInfo(); // Call the function when the page is opened
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromARGB(255, 1, 60, 120),
        title: Text('$uname',style:TextStyle(color: Color.fromARGB(255, 245, 250, 255))),  //replace username with el actual one men el data
        centerTitle: true,),
      body:
       SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: CircleAvatar(
                backgroundImage: AssetImage('assets/user_image.png'), // Replace with your image
                radius: 60,
              ),
            ),
            Padding(
              padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  buildDataField('Name', name), // Replace 'Test' with actual data
                  buildDataField('Date of Birth', dateOfBirth),
                  buildDataField('Gender', gender),
                  buildDataField('Chronic Illness', chronicIllness),
                  buildDataField('Previous Diagnosis', prevDiag),
                ],
              ),
            ),

          Align(
              alignment: Alignment.bottomRight,
              child: Padding(
                padding: EdgeInsets.all(20),
                child: OutlinedButton(
                  onPressed: () {
                    Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const HomePage(title: 'HomePage'))
                  );
                  },
                  style: OutlinedButton.styleFrom(
                    padding: EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                    side: BorderSide(color: Colors.red),
                  ),
                  child: Text(
                    'LOG OUT',
                    style: TextStyle(fontSize: 16, color: Colors.red),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    
  bottomNavigationBar: GNav(
        rippleColor: const Color.fromARGB(255, 129, 122, 122), // tab button ripple color when pressed
      hoverColor: Color.fromARGB(255, 240, 236, 236), // tab button hover color
       haptic: true, // haptic feedback
      tabBorderRadius: 30, 
    tabActiveBorder: Border.all(color: Colors.black, width: 1.5), // tab button border
    tabBorder: Border.all(color: Color.fromARGB(255, 191, 217, 246), width: 1), // tab button border
    tabShadow: [BoxShadow(color: Color.fromARGB(255, 191, 217, 246).withOpacity(0.5), blurRadius: 8)], // tab button shadow
    curve: Curves.easeOutExpo, // tab animation curves
    duration: Duration(milliseconds: 900), // tab animation duration
    gap: 8, // the tab button gap between icon and text 
    color: Color.fromARGB(255, 1, 75, 118), // unselected icon color
    activeColor: Color.fromARGB(255, 98, 163, 233), // selected icon and text color
    iconSize: 35, // tab button icon size
    tabBackgroundColor: Color.fromARGB(255, 191, 217, 246).withOpacity(0.1), // selected tab background color
    padding: EdgeInsets.symmetric(horizontal: 10, vertical: 5), // navigation bar padding
    tabs: [
      GButton(
      icon: LineIcons.user,
      text: 'Profile',
      ),
      GButton(
      icon: LineIcons.robot,
      text: 'Chat with Medhat',
      onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) =>  ChatScreen())
                  );
                }
      ),
      GButton(
      icon: LineIcons.newspaper,
      text: 'News',
      onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) =>  const FurtherInfoPage(title: 'FurtherInfoPage'))
                  );
                }
      )
      
  ]
      )    
      
    );
  }
  Widget buildDataField(String label, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: EdgeInsets.all(8.0),
          child: Text(
            '$label :',
            style: TextStyle(
              color: Color.fromARGB(255, 1, 60, 120),
              fontFamily: 'serif',
              fontWeight: FontWeight.bold,
              fontSize: 18,
            ),
          ),
        ),
        Padding(
          padding: EdgeInsets.all(8.0),
          child: Container(
            padding: EdgeInsets.all(12.0),
            decoration: BoxDecoration(
              border: Border.all(color: Colors.grey),
              borderRadius: BorderRadius.circular(8.0),
            ),
            child: Text(
              value , // Display the actual value from the database
              style: TextStyle(fontSize: 16, fontFamily: 'serif'),
            ),
          ),
        ),
      ],
    );
  }
  
}

class FurtherInfoPage extends StatelessWidget {
  const FurtherInfoPage({super.key, required this.title});

  final String title;

  _launchUrl(String linkURL) async {
    try {
      await launch(
        linkURL,
      );
      return true;
    } catch (e) {
      return false;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor:Color.fromARGB(255, 1, 60, 120) ,
        title: Text(title,style:TextStyle(color: Color.fromARGB(255, 252, 252, 253))),
      ),
      bottomNavigationBar: GNav(
        rippleColor: const Color.fromARGB(255, 129, 122, 122), // tab button ripple color when pressed
      hoverColor: Color.fromARGB(255, 240, 236, 236), // tab button hover color
       haptic: true, // haptic feedback
      tabBorderRadius: 30, 
    tabActiveBorder: Border.all(color: Colors.black, width: 1), // tab button border
    tabBorder: Border.all(color: Color.fromARGB(255, 191, 217, 246), width: 1.5), // tab button border
    tabShadow: [BoxShadow(color: Color.fromARGB(255, 191, 217, 246).withOpacity(0.5), blurRadius: 8)], // tab button shadow
    curve: Curves.easeOutExpo, // tab animation curves
    duration: Duration(milliseconds: 900), // tab animation duration
    gap: 8, // the tab button gap between icon and text 
    color: Color.fromARGB(255, 1, 75, 118), // unselected icon color
    activeColor: Color.fromARGB(255, 98, 163, 233), // selected icon and text color
    iconSize: 35, // tab button icon size
    tabBackgroundColor: const Color.fromARGB(255, 191, 217, 246).withOpacity(0.1), // selected tab background color
    padding: EdgeInsets.symmetric(horizontal: 10, vertical: 5), // navigation bar padding
    tabs: [
      GButton(
      icon: LineIcons.newspaper,
      text: 'News',
      ),
      GButton(
      icon: LineIcons.user,
      text: 'Profile',
      onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) =>  OptionPage())
                  );
                }
      ),
      GButton(
      icon: LineIcons.robot,
      text: 'Chat with Medhat',
      onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) =>  ChatScreen())
                  );
                }
      )
      
      
  ]
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'For further information, please refer to the following websites:',
              style: TextStyle(fontSize: 24, color: Color.fromARGB(255, 1, 60, 120)),
            ),
            buildLink('CDC (Centers for Disease Control and Prevention)', 'https://www.cdc.gov/media/archives.html', 'Visit the CDC website'),
            buildLink('NHS (National Health Service)', 'https://www.england.nhs.uk/news/', 'Visit the NHS website'),
            buildLink('MOHP (Ministry of Health and Populations of Egypt)', 'https://www.mohp.gov.eg/News.aspx', 'Visit the MOHP website')
          ],
        ),
      ),
    );
  }

  Widget buildLink(String linkText, String linkURL, String buttonText)
  {
    return Padding(
      padding: const EdgeInsets.all(14.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            linkText,
            style: const TextStyle(fontSize: 16 ),
          ),
          const SizedBox(height: 12),
          ElevatedButton(
            onPressed: () => _launchUrl(linkURL),
            child:
              Text(
                buttonText,
                style: const TextStyle(fontSize: 16,color: Color.fromARGB(255, 1, 60, 120)),
              ),
          )
        ],
      )
    );
  }
}

