const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = 3000;  // Frontend will run on port 3000

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Set EJS as templating engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// --- Routes --- //

// Home page - show list of books
app.get('/', async (req, res) => {
    try {
        const booksResponse = await axios.get('http://127.0.0.1:5000/books'); // Backend endpoint
        const books = booksResponse.data;
        res.render('index', { books: books });
    } catch (error) {
        console.error(error);
        res.send('Error fetching books');
    }
});

// Show create book form
app.get('/create-book', (req, res) => {
    res.render('create-book');
});

// Handle create book form
app.post('/create-book', async (req, res) => {
    try {
        await axios.post('http://127.0.0.1:5000/books', {
            title: req.body.title,
            author: req.body.author,
            genre: req.body.genre
        });
        res.redirect('/');
    } catch (error) {
        console.error(error);
        res.send('Error creating book');
    }
});

// Start frontend server
app.listen(PORT, () => {
    console.log(`Frontend Server running on http://127.0.0.1:${PORT}`);
});
