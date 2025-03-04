# Use the official Nginx image from the Docker Hub
FROM nginx:alpine

# Copy the HTML file to the Nginx HTML directory
COPY index.html /usr/share/nginx/html/

# Copy the MP4 video to the Nginx HTML directory
COPY scrolling.mp4 /usr/share/nginx/html/

# Copy the JavaScript file to the Nginx HTML directory
COPY js/optimize.js /usr/share/nginx/html/js/

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]