const mongoose = require('mongoose');

const venueSchema = new mongoose.Schema({
  name: String,
  capacity: Number,
  price: Number,
  // other venue details
});

const bookingSchema = new mongoose.Schema({
  venue: { type: mongoose.Schema.Types.ObjectId, ref: 'Venue' },
  // booking details
});

const Venue = mongoose.model('Venue', venueSchema);
const Booking = mongoose.model('Booking', bookingSchema);

module.exports = { Venue, Booking };
