import passport from 'passport';
import models from "../models/index.js";
import argon2 from 'argon2';
import jwt from 'jsonwebtoken';
import { addToBlacklist } from '../auth.js';
const { user } = models;

// Controller for user registration
export const register = async (req, res, next) => {
    try {
        const { username, email ,password } = req.body;

        const emailRegex = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
        if (!emailRegex.test(email)) {
            return res.status(400).json({ message: 'Invalid email format' });
        }

        const existingUserByUsername = await user.findOne({ where: { username } });
        if (existingUserByUsername) {
            return res.status(400).json({ message: 'Username already in use' });
        }

        const existingUserByEmail = await user.findOne({ where: { email } });
        if (existingUserByEmail) {
            return res.status(400).json({ message: 'Email already in use' });
        }

        const newUser = new user({ email, username, password, user_type: 'user' });
        try {
            await newUser.validate();
            await newUser.save();
        }
        catch (error) {
            return res.status(400).json({ message: error.message });
        }
        res.status(201).json({ message: 'Registration successful' });
    } catch (error) {
        next(error);
    }
};

// Controller for user login
export const login = async (req, res, next) => {
    try {
        const { username, password } = req.body;
        const userRecord = await user.findOne({ where: { username } });
        if (!userRecord) {
            return res.status(401).json({ message: 'Invalid credentials' });
        }
        const validPassword = await argon2.verify(userRecord.password, password);
        if (!validPassword) {
            return res.status(401).json({ message: 'Invalid credentials' });
        }
        const payload = { id: userRecord.id };
        const token = jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: '12h' });
        res.json({ token });
    } catch (error) {
        next(error);
    }
};

// Controller for user profile
export const profile = async (req, res, next) => {
    try {
        const profile = await user.findByPk(req.user.id);
        res.status(200).json({username: profile.username, email: profile.email, type: profile.user_type});
    } catch (error) {
        next(error);
    }
};

// Controller for user logout
export const logout = async (req, res, next) => {
    try {
        const token = req.headers.authorization.split(' ')[1]; // Assuming your token is in the format: Bearer <token>
        addToBlacklist(token);
        res.json({ message: 'User logged out successfully' });
    } catch (error) {
        next(error);
    }
};

// Controller for deleting a user
export const deleteUser = async (req, res, next) => {
    try {
        const { username } = req.params;
        const userRecord = await user.findOne({ where: { username } });
        if (!userRecord) {
            return res.status(404).json({ message: 'User not found' });
        }
        await userRecord.destroy();
        res.json({ message: 'User deleted successfully' });
    } catch (error) {
        next(error);
    }
};

export const changePassword = async (req, res) => {
    try {
        const userR  = req.user;
        const { oldPassword, newPassword } = req.body;
        const userRecord = await user.findByPk(userR.id);
        if (!userRecord) {
            return res.status(404).json({ message: 'User not found' });
        }
        const validPassword = await argon2.verify(userRecord.password, oldPassword);
        if (!validPassword) {
            return res.status(401).json({ message: 'Invalid credentials' });
        }
        await userRecord.update({ password: newPassword });

        res.json({ message: 'Password updated successfully' });
    } catch (error) {
        res.status(500).json({ message: "Internal server error" });
    }
};

export default { register, login, profile, logout, deleteUser, changePassword };