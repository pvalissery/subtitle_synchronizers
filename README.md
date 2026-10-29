
https://pvalissery.github.io/subtitle_synchronizers/

I watch a lot of foreign films, and half the time, the only subtitle I can find in a language I know is synced to a completely different release. It'll be perfectly timed for a WEBRip, but I'm watching a Blu-ray encode, and 20 minutes in, the text is a full three seconds behind the audio.

Adjusting the track synchronization in VLC works fine until the release has a different ad-break cut, and then everything is screwed up again. I got tired of guessing millisecond delays in Notepad, so I built a web tool to fix it visually.

##How it works:
You just drop in two files: a Reference SRT (a random sub in any language that is already perfectly synced to your video file) and your Target SRT (the unsynced one).

Scroll to a line you recognize. (Use google translate if you dont)

Click the dialogue in the reference file and then click the matching one in the unsynchronized file and hit apply.

The tool automatically calculates the exact millisecond offset between the two and shifts that specific target line and every single line after it. If there's a weird cut in the middle of the movie that throws the sync off again, you just scroll down, find the next matching line, and re-sync from there.

It’s just a single HTML file. No backend, no Python scripts to install, and your files never leave your machine since the whole thing processes locally in your browser.

