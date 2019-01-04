==========================
Random Level Select Tool
==========================

This tool allows for quick and customizable search of maps on atlas.dustforce.com


--------------------------
_config.json

This required file must be in the current working directory, and tells the program where several other files/folders are located:

	- "level_dir": the folder where custom maps are located
	- "index_file": the path to the json database file (will be created if one does not exist)
	- "rank_file": the path to the rank file used for populating the index (generated if the option is enabled)
	- "apple_rank_file": the path to the apple rank file used for populating the index (generated if the option is enabled)


--------------------------
create_index_gui.py (.exe)

This tool provides customization options for generating and updating the json database file.

	- "generate_rank_file" / "generate_apple_rank_file":
		These options pull custom level ranks from dustkid.com and store them in local files, for future use.
		This is an expensive operation, so only enable these if you really need up-to-date ranks.
	- "load_extended":
		searches for maps on atlas after the most recent map stored locally. Good for grabbing new maps
	- "load_missing":
		if a level ID does not have an associated local file, the map is downloaded from atlas
	- "reload_existing":
		re-downloads maps from atlas that are already stored locally. Mostly useless. Maybe useful if maps are corrupted?
	- "only_download_visible":
		as it says, only downloads visible maps off of atlas. skips hidden / unpublished maps
	- "debug":
		provides more verbose output


	- "lower_bound" / "upper_bound":
		only handles levels with IDs between these bounds, inclusively.
	- "min_missing_id":
		if load_missing is enabled, only tries to load missing levels with IDs higher than this value
	- "user_id":
		The dustkid.com ID number of the user. used for grabbing ranks when generate_rank_file is enabled
	- "update_map" / "add_map"
		adds information about the level itself to the database, such as if it has an end trigger
	- "update_ranks" / "add_ranks" / "update_apple_ranks" / "add_apple_ranks":
		adds rank info pulled from the generated ranks files into the database
	- "update_published" / "add_published":
		adds info about the status of the map on atlas to the database (visible / hidden / unpublished)

--------------------------
level_select_gui.py (.exe)

This tool uses the json database file to search for custom maps according to the user's configuration.

-- Buttons:
"Next" searches for candidates that match the given options, and chooses one
"Play" launches dustforce and starts the currently chosen level
"Atlas" and "Dustkid" load the respective web pages for the level

-- Results:
Once a level has been completed, the database can be updated by submitting results
"SS" updates the rank on that level
"SS_difficult" flags the level as difficult, and allows it to be filtered with options.
"ss_impossible" flags the level as impossible to SS, and allows it to be filtered with options.

A brief reason for why a level was flagged may be included before submitting.


-- Options:

Button options:
	each button can be set to "___", "NO", or "YES".
	"___" does no filtering
	"NO" excludes levels where the condition is True (e.g. SS "NO" only shows maps the player has not SS'd)
	"YES" excludes levels where the condition is False (e.g. SS "YES" only shows maps the player has SS'd)
Checkbox options:
	Can only be enabled or disabled
Text Entry options:
	Can take any string of characters

	- "completed" / "apple_completed":
		checks if the user already has a rank submitted on the level
	- "SS" / "apple_SS":
		checks if the user already has an SS rank submitted on the level
	- "SSable" / "apple_SSable":
		checks if it is possible to complete the level with an SS rank
		(if it has an end trigger, and hasnt been flagged as impossible)
	- "SS_difficult" / "apple_SS_difficult":
		checks if the level has been flagged as difficult previously
	- "has_end":
		checks if the level has an end trigger
	- "playable_type":
		checks if the map is Normal or Dustmod, as opposed to Multiplayer or Nexus types
	- "has_apples":
		checks if the level has any apples


	- "allow visible / hidden / unpublished / unknown":
		checks the status of the map on atlas. unknown is for maps whose status has not been recorded.
	- "choose_newest":
		picks the candidate with the largest map ID. usful for finding recent maps
	- "auto_launch":
		automatically launches dustforce when a map is chosen

	- "name_search":
		searches for the given string within the filename of a map (use dashes (-) to represent spaces)


