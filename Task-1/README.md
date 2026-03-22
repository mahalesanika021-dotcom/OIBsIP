# Task 1: Voice Assistant

## Description
In this task, I have created a basic voice assistant that recognizes user voice commands and responds accordingly. This assistant can perform simple tasks such as greeting, telling the time, telling the date, and performing web searches.

## Features
- Voice command recognition using Web Speech API
- Responds to "Hello" with a greeting
- Tells current time and date
- Opens web search for user queries
- User-friendly interface with microphone button
- Error handling for unrecognized commands

## Technologies Used
- HTML5
- CSS3
- JavaScript
- Web Speech API (Speech Recognition)

## How It Works
1. User clicks on the microphone button
2. Assistant listens to the voice command
3. Command is processed and appropriate action is taken
4. Assistant speaks back the response

## Voice Commands Supported
| Command | Action |
|---------|--------|
| "Hello" | Assistant responds with greeting |
| "What is the time?" / "Time" | Tells current time |
| "What is the date?" / "Date" | Tells current date |
| "Search for [query]" | Opens Google search for the query |

## Files
- `index.html` - Main structure of the voice assistant
- `style.css` - Styling and layout
- `script.js` - Voice recognition logic and command handling

## Future Enhancements
- Add more commands (weather, reminders, etc.)
- Natural language processing
- Integration with external APIs
