import test from 'node:test';import assert from 'node:assert/strict';import {playable,available} from './launch.mjs';
test('only a public credential-free play URL can be launched',()=>{assert.equal(playable('https://test.trycloudflare.com/play/'),'https://test.trycloudflare.com/play/');for(const url of ['http://test.trycloudflare.com/play/','https://evil.example/play/','https://test.trycloudflare.com.evil.example/play/','https://test.trycloudflare.com/play/?host=secret','https://test.trycloudflare.com/phone/','https://user:pass@test.trycloudflare.com/play/'])assert.throws(()=>playable(url));});

test('offline relay never counts as a playable destination',async()=>{
 assert.equal(await available('https://test.trycloudflare.com/play/',async()=>{throw Error('offline');}),false);
 assert.equal(await available('https://test.trycloudflare.com/play/',async()=>({ok:false})),false);
 assert.equal(await available('https://test.trycloudflare.com/play/',async()=>({ok:true,json:async()=>({service:'arcadelab-relay'})})),true);
});
