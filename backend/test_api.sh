#!/bin/bash

# Nepal Election System - API Test Script

BASE_URL="http://localhost:5000/api"

echo "🧪 Testing Nepal Election System API"
echo "======================================"

# 1. Add Candidates
echo -e "\n1️⃣ Adding candidates..."
curl -X POST $BASE_URL/candidate/add \
  -H "Content-Type: application/json" \
  -d '{"name":"Ram Bahadur Thapa","party":"Nepal Congress"}'

curl -X POST $BASE_URL/candidate/add \
  -H "Content-Type: application/json" \
  -d '{"name":"Sita Kumari Sharma","party":"CPN-UML"}'

# 2. List Candidates
echo -e "\n\n2️⃣ Listing candidates..."
curl -X GET $BASE_URL/candidate/list

# 3. Register Voter (requires actual files)
echo -e "\n\n3️⃣ Register voter (use frontend or provide actual files)"
echo "Example:"
echo "curl -X POST $BASE_URL/voter/register \\"
echo "  -F 'name=John Doe' \\"
echo "  -F 'dob=1990-01-01' \\"
echo "  -F 'citizenship_number=1234-5678-9012' \\"
echo "  -F 'citizenship_image=@/path/to/id.jpg' \\"
echo "  -F 'face_image=@/path/to/face.jpg'"

# 4. Check Voter Status
echo -e "\n\n4️⃣ Check voter status..."
echo "curl -X GET $BASE_URL/voter/status/1234-5678-9012"

# 5. Verify Voter
echo -e "\n\n5️⃣ Verify voter..."
echo "curl -X POST $BASE_URL/verify/verify/1"

# 6. Cast Vote
echo -e "\n\n6️⃣ Cast vote..."
echo "curl -X POST $BASE_URL/vote/cast \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"citizenship_number\":\"1234-5678-9012\",\"candidate_id\":1}'"

# 7. Get Results
echo -e "\n\n7️⃣ Getting results..."
curl -X GET $BASE_URL/vote/results

echo -e "\n\n✅ Test script completed"
