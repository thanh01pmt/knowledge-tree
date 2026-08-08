export default async (req, context) => {
  if (req.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405 });
  }

  try {
    const { messages } = await req.json();
    
    // Add a system prompt if needed
    const systemPrompt = {
      role: 'system',
      content: 'Bạn là một chuyên gia xây dựng lộ trình học tập (Roadmap Builder) cho hệ thống Knowledge Tree. Hãy trả lời ngắn gọn, súc tích và bằng tiếng Việt.'
    };
    
    // API Key từ Netlify Environment Variables
    // Có thể dùng process.env hoặc Netlify.env
    const apiKey = Netlify.env.get('DEEPSEEK_API_KEY');
    
    if (!apiKey) {
      return new Response(JSON.stringify({ error: 'Missing DEEPSEEK_API_KEY' }), { 
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Basic Rate Limiting check based on IP (Netlify provides x-nf-client-connection-ip)
    // For a real production app, you would use Redis or Supabase DB here.

    const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [systemPrompt, ...messages],
        stream: true
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      return new Response(JSON.stringify({ error: 'DeepSeek API Error', details: errorText }), {
        status: response.status,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Proxy the stream back to the client
    return new Response(response.body, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
      }
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), { 
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};

