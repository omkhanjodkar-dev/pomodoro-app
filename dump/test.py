from ai import analyze_youtube_content

# Analyze content
result = analyze_youtube_content(
    title="Python Programming Tutorial for Beginners",
    description="Learn Python programming from scratch..."
)

print(f"Is Distracting: {result['is_distracting']}")
print(f"Confidence: {result['confidence']}")
print(f"Recommendation: {result['recommendation']}")