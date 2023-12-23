import 'dart:convert';

import 'function.dart';
import 'package:flutter/material.dart';

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
        colorScheme: ColorScheme.fromSeed(seedColor: Color.fromARGB(255, 3, 25, 60)),
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
        title: Text(title),
      ),
      body: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const SizedBox(height: 16),
              OutlinedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const LogInPage(title: 'LogInPage')),
                  );
                },
              child: Text('Log In'),
              ),
              const SizedBox(height: 16),
              OutlinedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const CreateAccountPage(title: 'CreateAccountPage')),
                  );
                },
              child: Text('Create a new account'),
              )
          ],
        ),
        ),
    );
  }
}

class LogInPage extends StatelessWidget {
  const LogInPage({super.key, required this.title});

  final String title;

  @override
  Widget build(BuildContext context) {
    
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // TRY THIS: Try changing the color here to a specific color (to
        // Colors.amber, perhaps?) and trigger a hot reload to see the AppBar
        // change color while the other colors stay the same.
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
      ),
      body: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
             Text('Username'),
             const SizedBox(height: 8),
            const TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Type here...',
              ),
            ),
            Text('Password'),
            const SizedBox(height: 8),
            const TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Type here...',
              ),
            ),
            
            const SizedBox(height: 16),
            Center( // Center widget used here
              child: OutlinedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const MedhatPage(title: 'MedhatPage')),
                  );
                },
              child: Text('Log In'),
              )
            ),
          ],
        ),
      ),
    );
  }
}
    

class MedhatPage extends StatefulWidget {
  const MedhatPage({super.key, required this.title});
  final String title;
  @override
  
    State<MedhatPage> createState() => _MedhatPage();
  
}

class _MedhatPage extends State<MedhatPage> {
String url = '';
  var data;
  String output = 'Hi how are you?';
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
         title: Text(widget.title)),
      body:Center(
        child: Container(
          padding: EdgeInsets.all(20),
          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
            TextField(
              onChanged: (value) {
                url = 'http://127.0.0.1:5000/api?query=' + value.toString();
              },
            ),
            TextButton(
                onPressed: () async {
                  data = await fetchdata(url);
                  var decoded = jsonDecode(data);
                  setState(() {
                    output = decoded['output'];
                  });
                },
                child: Text(
                  'Get a response',
                  style: TextStyle(fontSize: 20),
                )),
            Text(
              output,
              style: TextStyle(fontSize: 40, color: Colors.green),
            )
          ]),
        ),
      ),
    );
  }
}

class CreateAccountPage extends StatelessWidget {
  const CreateAccountPage({Key? key, required this.title}) : super(key: key);
  final String title;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
      ),
      body: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
             Text('Name'),
             const SizedBox(height: 8),
            const TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Type here...',
              ),
            ),
            Text('Date of birth'),
            const SizedBox(height: 8),
            const TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Type here...',
              ),
            ),
            Text('Gender'),
            const SizedBox(height: 8),
            const TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Type here...',
              ),
            ),
            Text('Chronic Illness'),
            const SizedBox(height: 8),
            const TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Type here...',
              ),
            ),
            const SizedBox(height: 16),
            Center( // Center widget used here
              child: OutlinedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const MedhatPage(title: 'MedhatPage')),
                  );
                },
              child: Text('Create account'),
              )
            ),
          ],
        ),
      ),
    );
  }
}

class AccountPage extends StatelessWidget {
  const AccountPage({Key? key, required this.title}) : super(key: key);
  final String title;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
      ),
      body: Align(
        alignment: Alignment.bottomRight,
        child: OutlinedButton(
          onPressed: () {Navigator.pop(context, "Logged out successfully");},
          child: const Text('Log out'),
        ),
      ),
    );
  }
}