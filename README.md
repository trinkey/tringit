# Trin-git
A git-like program built for the website [trinket.io](https://trinket.io/)

### NOTE: THIS PROGRAM IS MADE FOR WINDOWS AND LINUX.
I cannot guarentee that this works on Mac, as I don't have a device running MacOS to test it on.

# How to use
When you first run the program, it will prompt you to input your cookie. This can be found in most requests in inspect element.

To find it, open inspect element (Ctrl+Shift+I, or F12), and to go the network tab.

![image](https://github.com/trinkey/tringit/assets/97406176/90ce4bc6-0cb8-4a52-b6ae-33e5fdaa977c)

Next, go to your [trinket library](https://trinket.io/library/trinkets), and look for a request that has the name of something along the lines of `trinkets?limit=20&sort=xyz`. Once you find it, click on it.

(In firefox, the `trinkets?limit=20...` request will be under the `File` tab, unline `Name` in Chromium-based browsers)

![image](https://github.com/trinkey/tringit/assets/97406176/737481dc-2ca5-421d-8ccc-fc8c4963cab9)

When you click on it, make sure you are on the headers tab of the request info, and then scroll down to the section labeled `Request Headers`. Inside should be an item labelled `Cookie`. Copy the value of that and paste it into the program.

Next, it asks for the trinket id, which is the part in the url for a trinket after the `https://trinket.io/library/trinkets/`, for example `7df117b053` would be from `https://trinket.io/library/trinkets/7df117b053`. This will be the selected trinket, and you can change this later.

Everything else after that should be pretty self-explanatory. If the trinket has a file with the same name as the tringit file, tringit will be overwritten.
