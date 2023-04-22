Sure, here's the transformed code in Express.js:

const express = require('express');
const router = express.Router();
const { User } = require('../models');
const { hash } = require('../utils');
const { body, validationResult } = require('express-validator');

// CREATING USERS:

router.post('/users', [
  body('email').isEmail(),
  body('password').isStrongPassword(),
  body('username').isLength({ min: 1, max: 20 }),
], async (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(422).json({ errors: errors.array() });
  }

  const { email, password, username } = req.body;
  const hashedPassword = hash(password);

  try {
    let user = await User.findOne({ email });
    if (user) {
      return res.status(409).json({ message: `This email: ${email} is already registered. Please use another email or renew your password for this one.` });
    }

    user = await User.findOne({ username });
    if (user) {
      return res.status(409).json({ message: `This username: ${username} is already taken. Please choose another username.` });
    }

    const newUser = new User({ email, password: hashedPassword, username });
    await newUser.save();

    res.status(201).json(newUser);
  } catch (err) {
    next(err);
  }
});

module.exports = router;


A few notes on the transformation:
- Express.js uses middleware functions to handle requests, so we use `body` and `validationResult` middleware from the `express-validator` package to validate the request body.
- We use `async/await` syntax to handle asynchronous operations like querying the database and saving the new user.
- We use `try/catch` blocks to handle errors and pass them to the error handling middleware using `next(err)`.
- We use `module.exports` to export the router object for use in our main Express app.