1st  assignment (DIY BOT)

Ανδρονούδης Δήμος

MusicBot

Ο κύριος λόγος που δημιούργησα ένα Rasachatbot με κύριο θέμα τη μουσική, είναι επειδή πιστεύω πως οι προτάσεις που κάνουν πλατφόρμες όπως το YouTube και το Spotify 
και αφορούν παρόμοια τραγούδια σε στιλ και ύφος, δεν είναι ιδιαίτερα καλές. 
Για αυτόν τον λόγο θα ήθελα να δω την διαδικασία πίσω από αυτές τις επιλογές και η εν λόγω εργασία πιστεύω ότι μου δίνει μία τέτοια δυνατότητα.

**Σενάρια**

Τα τρία σενάρια που δημιούργησα είναι :

 1ο happy path:
 Ελεύθερο στο bot να κατευθύνει τη διαδικασία αναζήτησης μουσικής δίνοντας απλά το είδος, με το όνομα "Surprise\_me". 
 Tο action.py αρχείο βασίζεται στις επιλογές του χρήστη στο είδος της μουσικής που τα δώσει ως input ανάμεσα σε funk, rock, pop και επιστρέφει έναν/μία τυχαίο/α καλλιτέχνη από τις τρεις εκάστοτε λίστες. 
 Σε επόμενο στάδιο θα μπορούσε να συνδέεται με μία βάση δεδομένων που βρίσκονται ήδη κατηγοριοποιημένα όλα και να συλλέγει από εκεί τις πληροφορίες. 
 Επίσης θα μπορούσε να προτείνει και τραγούδια με βάση τον/την καλλιτέχνη. Τέλος θα έπρεπε να ενεργοποιεί το play του εκάστοτε τραγουδιού.

 2ο happy path:
 Ο χρήστης κατευθύνει την διαδικασία αναζήτησης μουσικής με το όνομα "my\_music\_my\_rules", δίνοντας αυτή τη φορά το όνομα της μπάντας.

 3οsadpath:
 Ο χρήστης δεν καταφέρνει να βρει αυτό που επιθυμεί με το όνομα "not\_enough\_info". 
 Ο χρήστης ζητάει μουσική στο ύφος του τραγουδιού που του προτάθηκε εξ αρχής από το bot χρησιμοποιώντας και πάλι το action. 
 Αντίθετα όμως με τον πρώτο διάλογο, το επόμενο τραγούδι στο cd δεν είναι στο ίδιο ύφος του προηγούμενου με τον χρήστη να εκφράζει την δυσαρέσκεια και το bot να ζητάει συγγνώμη.

**Αδυναμίες και μελλοντικές βλέψεις**

Έγινε χρήση μόνο καλλιτεχνών και ειδών μουσικής, αλλά όχι μεμονωμένων τραγουδιών. Σε επόμενο στάδιο πρέπει να γίνει χρήση database για επιλογή τραγουδιών, καλλιτεχνών και ειδών. 
Ιδανικά θα μπορούσε να γίνεται σύνδεση του bot με κάποιο app (spotify), ή να λειτουργεί σαν add-on σε αυτό.

Μία χαρακτηριστική αδυναμία του μοντέλου είναι πως δεν αναγνωρίζει το entity όταν αναφέρεται μέσω προσωπικής αντωνυμίας σε επόμενη ερώτηση/απάντηση (π.χ. "Ilikeit, givememoreofthem").

 Χρήση επιμέρους πληροφοριών metadata των τραγουδιών για καλύτερη εξυπηρέτηση. 
 Χρησιμοποιώντας ως παράδειγμα το sadpath που έφτιαξα, φαίνεται πως η επιλογή τραγουδιού πρέπει να συμβαδίζει με την ανάγκη του ακροατή. 
 Έτσι η απλή συνέχεια της μουσικής ενός καλλιτέχνη, δεν προϋποθέτει την κάλυψη της ανάγκης του ακροατή, καθώς η μουσική του υποτιθέμενου καλλιτέχνη στο παράδειγμα δεν ακολουθεί το ίδιο ύφος πάντοτε. 
 Έτσι, η επιλογή ενός τραγουδιού θα πρέπει να γίνεται συνδυάζοντας επιμέρους πληροφορίες.

Σε μερικές περιπτώσεις δεν αποθηκευόταν η πληροφορία της μπάντας, και επιστρέφει none. 
Αυτό συμβαίνει όπου παρεμβάλλεται action. Σε άλλα παραδείγματα επέστρεφε κανονικά, σας επισυνάπτω ένα printscreen του δεύτερου διαλόγου.

**Παραδείγματα διαλόγων από το**  **Rasa**

1st story - happy (surprise\_me)

Your input -\> hi

Hello! Ready to kick off your day with some tunes. What's your musical mood today?

Your input -\> play some rock music

Sure! I'll play some rock by Nirvana.

Your input -\> Do you have any more music in this style?

I'm glad you liked it! None has a few more tracks in their latest album. Would you like to continue with them, or do you want to explore a different artist?

Your input -\> Let's stick with Nirvana for now. What's the next track?

Keeping the None going! Let's go to the next

2nd story - happy (my\_music\_my\_rules)

Your input -\> hi

Hello! Ready to kick off your day with some tunes. What's your musical mood today?

Your input -\> I want to listen to Queen

Okay so... lets go with Queen

Your input -\> That's perfect give me more

I'm glad you liked it! Queen has a few more tracks in their latest album. Would you like to continue with them, or do you want to explore a different artist?

Your input -\> Let's stick with Qeen

Keeping the Qeen going! Let's go to the next

3rd story -unhappy (not\_enough\_info)

Your input -\> hi

Hello! Ready to kick off your day with some tunes. What's your musical mood today?

Your input -\> i'm in the mood for pop

Sure! I'll play some pop by Madonna.

Your input -\> I like it

I'm glad you liked it! None has a few more tracks in their latest album. Would you like to continue with them, or do you want to explore a different artist?

Your input -\> Let's stick to Madonna

Okay so... lets go with Madonna

Your input -\> It feels like this song doesn't quite match the mood set by the previous one

I'm sorry. Do you want to explore a different artist?

![](RackMultipart20231112-1-51iogw_html_f2c3c1dc3ef5e369.png)# rasa_bot![all good](https://github.com/DimosAndronoudis/rasa_bot/assets/106241599/b9e73990-401a-4b06-8245-27f0dd99e554)
