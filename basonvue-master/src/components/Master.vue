<template>
    <div class="mx-3 mb-3 mt-5 master-control">
        <div style="display: flex"> 
            <div style="display: flex; flex-direction: column">
                <img  :src="imageLogo" style="width: 104.7px; height:30px; margin-top: -90px;"/>
                <img  :src="imageLogoEnib" style="width: 104.7px; height:44px; margin-top: 5px; border-radius: 7px; background-color: white; border: 5px solid white"/>
            </div>
            <div>
                <p style="color: ghostwhite; margin-top: -85px; margin-left: 20px; font-size: 40px">BaSon</p>
            </div>
        </div>
        <span class="master-control-label control-label">MASTER CONTROL</span>
        <div style="display: flex; width: 100%; margin: 20px auto 10px 0px; justify-content: center">
            <div class="" style="display:block; padding: 2rem 1rem" >
                <div style="display: flex; margin-bottom: 25px; border: 2px solid rgb(96, 100, 105); padding: 0.6em; border-radius: 0.5rem; position: relative">
                    <span class="control-label">PLAY</span>
                    <div style='margin-right: 20px'>
                        <button class="btn btn-success buttonAction shadow-none btn-style" id="btnPlay" type="button" @click="changeButtonAction">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-play-fill" viewBox="0 0 16 16" style="margin-top:2px">
                                <path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/>
                            </svg>
                        </button>
                        <button class="btn btn-danger buttonAction d-none shadow-none btn-style" id="btnPause" type="button" @click="changeButtonAction">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-stop-fill" viewBox="0 0 16 16" style="margin-top:2px">
                                <path d="M5 3.5h6A1.5 1.5 0 0 1 12.5 5v6a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 11V5A1.5 1.5 0 0 1 5 3.5z"/>
                            </svg>
                        </button>
                    </div>

                    <div class="divInputBpm" style='margin-right: 20px' id="bpmGroup">
                        <label class="labelInputBpm" color="gray" font-size="0.6rem" font-weight="600" letter-spacing="0.1em" for="bpm">BPM</label>
                        <input class="bpm-text-input inputBpm" min="30" max="300" font-size="1.5rem" font-weight="500" id="bpm" color="brightRed" type="number" v-model.number="bpm"  @blur="updateInput">
                        <div class="divInputButtons" display="flex">
                            <button class="inputButton" id="inputButtonUp" color="white" width="2rem" aria-label="Increase beat per minute" font-weight="bold" @mousedown="upBpm(true)" @mouseup="resetMouseDown">
                                <svg width="10px" height="6px" viewBox="0 0 12 7" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink">
                                    <polygon points="0 7 12 7 6 0" fill="white"></polygon>
                                </svg>
                            </button>
                            <button class="inputButton" id="inputButtonDown" color="white" width="2rem" aria-label="Decrease beat per minute" font-weight="bold" @mousedown="downBpm(true)" @mouseup="resetMouseDown">
                                <svg width="10px" height="6px" viewBox="0 0 12 7" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink">
                                <polygon points="0 0 12 0 6 7" fill="white"></polygon>
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div class="divInputBpm" id="nbBeatsGroup">
                        <label class="labelInputBpm" color="gray" font-size="0.6rem" font-weight="600" letter-spacing="0.1em" for="nbBeats">BPLoop  </label>
                        <input class="bpm-text-input inputBpm" min="30" max="300" font-size="1.5rem" font-weight="500" id="nbBeats" color="brightRed" type="number" v-model.number="nbBeats"  @blur="updateInputNbBeats" style="margin-left:5px;width: 50px">
                        <div class="divInputButtons" display="flex">
                            <button class="inputButton" id="inputButtonUpNbBeats" color="white" width="2rem" aria-label="Increase beat per minute" font-weight="bold" @mousedown="upNbBeats()">
                                <svg width="10px" height="6px" viewBox="0 0 12 7" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink">
                                    <polygon points="0 7 12 7 6 0" fill="white"></polygon>
                                </svg>
                            </button>
                            <button class="inputButton" id="inputButtonDownNbBeats" color="white" width="2rem" aria-label="Decrease beat per minute" font-weight="bold" @mousedown="downNbBeats()">
                                <svg width="10px" height="6px" viewBox="0 0 12 7" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink">
                                <polygon points="0 0 12 0 6 7" fill="white"></polygon>
                                </svg>
                            </button>
                        </div>
                    </div>
                    

                </div>
                <div style="display: flex;">

                    <div class="knob-slot" style="margin-right: 90px">
                        <span class="knob-name">VOL</span>
                        <div class="knob">
                            <span class="knob-label">0</span>
                            <webaudio-knob
                                :src="volKnobData.imageURL"
                                :min="volKnobData.min"
                                :max="volKnobData.max"
                                :width="volKnobData.size"
                                :height="volKnobData.size"
                                :value="100"
                                :id="'volumeMaster'"
                                @input="updateGainMaster"
                                @dblclick="resetGainMaster"
                                :valuetip="1">
                            </webaudio-knob>
                            <span class="knob-label">1</span>
                        </div>
                    </div>
                    <div style="border: 2px solid rgb(96, 100, 105); padding: 0.6em; border-radius: 0.5rem; position: relative">
                        <span class="control-label">RECORD</span>
                        <div class="divInputBpm" style="width: 144px;">
                            <div style="display: flex">
                                <label class="labelInputBpm" color="gray" font-size="0.6rem" font-weight="600" letter-spacing="0.1em" for="nbRecord">Loop Record</label>
                                <input class="bpm-text-input inputBpm" min="30" max="300" font-size="1.5rem" font-weight="500" id="nbRecord" color="brightRed" type="number" v-model.number="nbRecord"  @blur="updateInputNbRecord" style="margin-left:15px;width: 40px">
                                <div class="divInputButtons" display="flex">
                                    <button class="inputButton" id="inputButtonUpNbRecord" color="white" width="2rem" aria-label="Increase beat per minute" font-weight="bold" @mousedown="upNbRecord()">
                                        <svg width="10px" height="6px" viewBox="0 0 12 7" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink">
                                            <polygon points="0 7 12 7 6 0" fill="white"></polygon>
                                        </svg>
                                    </button>
                                    <button class="inputButton" id="inputButtonDownNbRecord" color="white" width="2rem" aria-label="Decrease beat per minute" font-weight="bold" @mousedown="downNbRecord()">
                                        <svg width="10px" height="6px" viewBox="0 0 12 7" version="1.1" xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink">
                                        <polygon points="0 0 12 0 6 7" fill="white"></polygon>
                                        </svg>
                                    </button>
                                </div>
                                <div class="gradient" style="margin: -2px 0 0 3px">
                                    <button type="button" class="btn buttonActionRecord shadow-none" @click="startRecord" id="recorderButton" style="background-color: #1F1F1F; border: 2px solid rgb(96, 100, 105); border-radius: 0.5rem; border-right-width: 0px; border-top-left-radius: 0; border-bottom-left-radius: 0">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" class="bi bi-record-fill" viewBox="0 0 16 16" style="margin-top:2px" id="circleRecord">
                                            <path fill-rule="evenodd" d="M8 13A5 5 0 1 0 8 3a5 5 0 0 0 0 10z"/>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
            <div class="divMasterScope">
                <MasterScope />
            </div>
            <div style='display: block; padding: 0rem 1rem' class="divConfig">

                <div style="margin-bottom: 40px">
                    <AddSampleBtn />
                </div>

                <div style="margin-bottom: 40px; style: flex">
                    <button type="button" class="btn btn-secondary btn-demo shadow-none btn-style" @click="setInDemo">
                        <div style="display: flex">
                            <div style="margin-top:3px">
                                <p style="margin: 5px 15px 0 0px">DEMO</p>
                            </div>
                            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-headphones" viewBox="0 0 16 16" style="margin: 2px 0 0 0">
                                <path d="M8 3a5 5 0 0 0-5 5v1h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V8a6 6 0 1 1 12 0v5a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1V8a5 5 0 0 0-5-5z"/>
                            </svg>
                        </div>
                    </button>
                    <button type="button" class="btn btn-secondary mybtn-info shadow-none btn-style" style="border-radius: 50%; margin-left: 15px" data-bs-toggle="modal" data-bs-target="#modalInfo">
                        <div style="display: flex">
                            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-info" viewBox="0 0 16 16">
                                <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
                            </svg>
                        </div>
                    </button>
                    <div class="modal fade" id="modalInfo" tabindex="-1" aria-labelledby="modalInfoLabel" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-info">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="exampleModalLabel">Info</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <p>Ce projet a été réalisé par Antoine Brusco et Tinaël Sanvoisin lors d'un projet universitaire de quatrième année à l'ENIB (Ecole Nationale d'Ingénieurs de Brest) sous le tutorat de Gireg Desmeulles et Vincent Choqueuse.
                                       <br/>Ce site a été développé pour l'association "Vivre Le Monde" afin d'être utilisé dans des interventions qui ont pour objectif d'éveiller les jeunes, dans des écoles et collèges, à la musique par la création de séquences rythmiques.
                                    </p>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" id="stopModal" data-bs-dismiss="modal">Retour</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="display: flex; height:52px;">
                    <div>
                        <label for="fileJson" class="btn btn-secondary buttonActionLoad btn-style" @click="loadingFile" style="display: flex; border-bottom-right-radius: 0px; border-top-right-radius: 0px;">
                            <!-- Generator: Adobe Illustrator 17.1.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
                            <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
                            <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                                viewBox="0 0 276.157 276.157" style="enable-background:new 0 0 276.157 276.157;" xml:space="preserve">
                            <path style="fill:#FFF;" d="M273.081,101.378c-3.3-4.651-8.86-7.319-15.255-7.319h-24.34v-26.47c0-10.201-8.299-18.5-18.5-18.5
                                h-85.322c-3.63,0-9.295-2.876-11.436-5.806l-6.386-8.735c-4.982-6.814-15.104-11.954-23.546-11.954H58.731
                                c-9.293,0-18.639,6.608-21.738,15.372l-2.033,5.752c-0.958,2.71-4.721,5.371-7.596,5.371H18.5c-10.201,0-18.5,8.299-18.5,18.5
                                v167.07c0,0.885,0.161,1.73,0.443,2.519c0.152,3.306,1.18,6.424,3.053,9.064c3.3,4.652,8.86,7.319,15.255,7.319h188.486
                                c11.395,0,23.27-8.424,27.035-19.179l40.677-116.188C277.061,112.159,276.381,106.03,273.081,101.378z M18.5,64.089h8.864
                                c9.295,0,18.64-6.608,21.738-15.372l2.032-5.75c0.959-2.711,4.722-5.372,7.597-5.372h29.564c3.63,0,9.295,2.876,11.437,5.806
                                l6.386,8.734c4.982,6.815,15.104,11.954,23.546,11.954h85.322c1.898,0,3.5,1.603,3.5,3.5v26.47H69.34
                                c-11.395,0-23.27,8.424-27.035,19.179L15,191.231V67.589C15,65.692,16.603,64.089,18.5,64.089z M260.791,113.238l-40.677,116.188
                                c-1.674,4.781-7.812,9.135-12.877,9.135H18.751c-1.448,0-2.577-0.373-3.02-0.998c-0.443-0.625-0.423-1.814,0.056-3.181
                                l40.677-116.188c1.674-4.781,7.812-9.135,12.877-9.135h188.486c1.448,0,2.577,0.373,3.021,0.998
                                C261.29,110.682,261.27,111.871,260.791,113.238z"/>
                            </svg>
                        </label>
                        <input id="fileJson" style="visibility:hidden; width: 0px; height: 0px" type="file" accept="application/json" @change="readFile">
                    </div>
                    <div>
                        <label for="fileJsonSave" class="btn btn-secondary buttonActionLoad btn-style" @click="activeModal" style="display: flex; border-bottom-left-radius: 0px; border-top-left-radius: 0px;">
                            <!-- Generator: Adobe Illustrator 19.0.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
                        <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                            viewBox="0 0 469.333 469.333" style="enable-background:new 0 0 469.333 469.333; fill: white" xml:space="preserve">
                            <g>
                                <g>
                                    <g>
                                        <path d="M466.208,88.458L380.875,3.125c-2-2-4.708-3.125-7.542-3.125H42.667C19.146,0,0,19.135,0,42.667v384
                                            c0,23.531,19.146,42.667,42.667,42.667h384c23.521,0,42.667-19.135,42.667-42.667V96
                                            C469.333,93.167,468.208,90.458,466.208,88.458z M106.667,21.333h234.667v128c0,11.76-9.563,21.333-21.333,21.333H128
                                            c-11.771,0-21.333-9.573-21.333-21.333V21.333z M384,448H85.333V256H384V448z M448,426.667c0,11.76-9.563,21.333-21.333,21.333
                                            h-21.333V245.333c0-5.896-4.771-10.667-10.667-10.667h-320c-5.896,0-10.667,4.771-10.667,10.667V448H42.667
                                            c-11.771,0-21.333-9.573-21.333-21.333v-384c0-11.76,9.563-21.333,21.333-21.333h42.667v128C85.333,172.865,104.479,192,128,192
                                            h192c23.521,0,42.667-19.135,42.667-42.667v-128h6.25L448,100.417V426.667z"/>
                                        <path d="M266.667,149.333h42.667c5.896,0,10.667-4.771,10.667-10.667V53.333c0-5.896-4.771-10.667-10.667-10.667h-42.667
                                            c-5.896,0-10.667,4.771-10.667,10.667v85.333C256,144.562,260.771,149.333,266.667,149.333z M277.333,64h21.333v64h-21.333V64z"
                                            />
                                    </g>
                                </g>
                            </g>
                        </svg>
                        </label>
                        <a id="fileJsonSave" style="visibility:hidden;" href=""></a>
                    </div>

                    <!-- Button trigger modal -->
                    <button type="button" class="btn btn-primary d-none" id="saveFileName" data-bs-toggle="modal" data-bs-target="#modalName">
                    </button>

                    <!-- Modal -->
                    <div class="modal fade" id="modalName" tabindex="-1" aria-labelledby="modalNameLabel" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="exampleModalLabel">Sauvegarde du pattern</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <label for='nameFile' style="margin-right: 15px">Nom du fichier :</label>
                                    <input id="nameFile" type="text"/>
                                    <p class="text-danger mt-2" style="margin: 0; font-weight: bold">Attention les samples ne seront pas sauvegardés. Il faudra les récupérer sur <a href="https://banana-cobbler-95780.herokuapp.com">ce site</a>.</p>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" id="stopModal" data-bs-dismiss="modal">Retour</button>
                                    <button type="button" class="btn btn-success" @click="writeFile">Sauvegarder</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Button trigger modal -->
                    <button type="button" class="btn btn-primary d-none" id="saveFileNameRecord" data-bs-toggle="modal" data-bs-target="#modalNameRecord">
                    </button>

                    <!-- Modal -->
                    <div class="modal fade" id="modalNameRecord" tabindex="-1" aria-labelledby="modalNameLabelRecord" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="exampleModalLabel">Télécharger le fichier audio</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <label for='nameFileRecord' style="margin-right: 15px">Nom du fichier :</label>
                                    <input id="nameFileRecord" type="text"/>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" id="stopModal" data-bs-dismiss="modal">Retour</button>
                                    <button type="button" class="btn btn-success" data-bs-dismiss="modal" @click="recordFile">Télécharger</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <a class="d-none" href="" id="saveRecordFileA"></a>
            </div>
            <div class="position-fixed top-0 p-3" style="z-index: 5; left: 40%">
                <div id="liveToast" class="toast hide" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="toast-header">
                    <strong class="me-auto">Info</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                    <div class="toast-body">
                    <p style="margin:0">N'oubliez pas : les samples ne sont pas sauvegardés dans le fichier !</p>
                    </div>
                </div>
            </div>
            <div class="position-fixed top-0 p-3 text-danger" style="z-index: 5; left: 40%">
                <div id="issueToast" class="toast hide" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="toast-header">
                    <strong class="me-auto">Fichier non conforme !</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                    <div class="toast-body">
                    <p style="margin:0">Votre fichier est endommagé et ne peut pas être lu !</p>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
</template>

<script>
import MasterScope from '@/components/MasterScope.vue'
import AddSampleBtn from '@/components/AddSampleBtn.vue'
import CustomSelect from "@/components/CustomSelect.vue";
import '@/assets/js/webaudio-controls.js'
import volKnobImage from '@/assets/images/knobs/maschine-default.png'
export default ({
    name: "Master",
    components: {
        MasterScope,
        AddSampleBtn,
        CustomSelect,
    },
    data(){
        return{
            mouseDown: false,
            allNbBeats: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'],
            currentBeat: '4',
            allNbBeatsRecord: ['1', '2', '3' , '4'],
            volKnobData: {imageURL:volKnobImage, min:0, max:100, size:40, drawWaveformRequest: null, drawFrequencyBarRequest: null},
            imageLogo: require('../assets/images/LOGO_TEXTE_blanc.png'),
            imageLogoEnib: require("../assets/images/ENIB-logo.png")
        }
    },
    computed: { 
        currentNbBeatsRecord(){
            return this.$store.state.nbBeatsRecord.toString();
        },
        getAudioCtx(){
            return this.$store.getters.getAudioCtx;
        },
        bpm: {
            get(){
                return this.$store.state.bpm;
            },
            set(newBpm){
                if(newBpm > 300){
                    newBpm = 300;
                    this.$store.commit("setBpm", newBpm);
                    this.$forceUpdate();
                    return;
                }
                else if(newBpm < 30){
                    newBpm = 30;
                }
                this.$store.commit("setBpm", newBpm);
                
            }
        },
        nbRecord:{
            get(){
                return this.$store.state.nbBeatsRecord;
            },
            set(newNbRecord){
                if(newNbRecord > 4){
                    newNbRecord = 4;
                    this.$store.commit("updateNbBeatsRecord", newNbRecord);
                    this.$forceUpdate();
                    return;
                }
                else if(newNbRecord < 1){
                    newNbRecord = 1;
                }
                this.$store.commit("updateNbBeatsRecord", newNbRecord);
            }
        },
        nbBeats:{
            get(){
                return this.$store.state.nbBeats;;
            },
            set(newNbBeats){
                if(newNbBeats > 16){
                    newNbBeats = 16;
                    this.$store.commit("updateNbBeats", newNbBeats);
                    this.$forceUpdate();
                    return;
                }
                else if(newNbBeats < 1){
                    newNbBeats = 1;
                }
                this.$store.commit("updateNbBeats", newNbBeats);
            }
        },
    },
    methods: {
        updateGainMaster(){
            var value = document.getElementById("volumeMaster").value/100;
            this.$store.commit("updateGainMaster", value);
        },
        loadingFile(){
            document.getElementById("fileJson").click();
        },
        setSequenceur(data, demo=false){
                var jsonData = data;
                if(jsonData.bpm){
                    if(jsonData.bpm>=30 && jsonData.bpm<=300){
                        this.$store.commit("setBpm", jsonData.bpm);
                    }
                }
                if(jsonData.masterVolume){
                    if(jsonData.masterVolume <= 1 && jsonData.masterVolume >=0){
                        this.$store.commit('updateGainMaster', jsonData.masterVolume);
                        document.getElementById("volumeMaster").setValue(jsonData.masterVolume*100);
                    }
                }
                if(jsonData.nbTemps){
                    if(jsonData.nbTemps>=1 && jsonData.nbTemps<=16){
                        this.$store.commit("updateNbBeats", jsonData.nbTemps);
                    }
                }
                if(jsonData.nbRecord){
                    if(jsonData.nbRecord>=1 && jsonData.nbRecord<=4){
                        this.$store.commit("updateNbBeatsRecord", jsonData.nbRecord);
                    }
                }
                this.$store.commit("resetSamplesChosen");
                setTimeout(()=>{jsonData.channels.forEach(sample => {
                    try{
                        this.$store.commit('addSamplesChosen', {sampleName: sample.name, src: sample.src});
                        
                        this.$store.state.samplesChosen[sample.id-1].track = sample.track;
                        this.$store.state.samplesChosen[sample.id-1].timeSubdiv = sample.nbSubDiv;
                        this.$store.state.samplesChosen[sample.id-1].frequencyInTime = sample.frequencyInTime;
                        this.$store.state.samplesChosen[sample.id-1].audioNode.filter.type = sample.filterType;
                        this.$store.state.samplesChosen[sample.id-1].filterName = sample.filterName;
                        this.$store.state.samplesChosen[sample.id-1].filterColor = sample.filterColor;
                        this.$store.state.samplesChosen[sample.id-1].audioNode.filter.frequency.setValueAtTime(sample.frequency, this.$store.state.audioCtx.currentTime);
                        this.$store.state.samplesChosen[sample.id-1].audioNode.filter.Q.setValueAtTime(sample.Q, this.$store.state.audioCtx.currentTime);
                        setTimeout(()=>{
                            document.getElementById("freq"+sample.id).setValue(Math.log10(sample.frequency/20));
                            document.getElementById("Q"+sample.id).setValue(sample.Q);
                            this.$store.commit("updateGain", {value: sample.volume, sampleId: sample.id});
                            document.getElementById("volume"+sample.id).setValue(sample.volume*100);
                            this.$store.commit("updatePan", {value: sample.pan, sampleId: sample.id});
                            document.getElementById("pan"+sample.id).setValue(sample.pan*100);
                            document.getElementById("nbSubDiv"+sample.id).innerHTML = sample.nbSubDiv;
                            for(var i=0; i<this.$store.state.nbBeats*sample.nbSubDiv; i++){
                                var id = i%sample.nbSubDiv + 1 + this.$store.state.samplesChosen[sample.id-1].timeSubdiv*(Math.ceil((i+1)/sample.nbSubDiv)-1);
                                var temps = "temps-ref-"+this.$store.state.samplesChosen[sample.id-1].id.toString()+'-'+id.toString();
                                if(this.$store.state.samplesChosen[sample.id-1].track[i].gain===1){
                                    document.getElementById(temps).classList.add("active1");
                                }
                                else if(this.$store.state.samplesChosen[sample.id-1].track[i].gain===0.5){
                                    document.getElementById(temps).classList.add("active2");
                                }
                                else if(this.$store.state.samplesChosen[sample.id-1].track[i].gain===0.25){
                                    document.getElementById(temps).classList.add("active3");
                                }
                            }
                            if(!demo){
                                document.getElementById("liveToast").classList.remove("hide");
                                document.getElementById("liveToast").style.transition= "opacity 0.3s";
                                document.getElementById("liveToast").style.opacity = 1;
                                setTimeout(()=>{
                                    document.getElementById("liveToast").style.opacity = 0;
                                    setTimeout(()=>{document.getElementById("liveToast").classList.add("hide")},300)
                                },4000)
                            }
                        }, 100)
                    }
                    catch{
                        setTimeout(()=> {
                            this.$store.commit("resetSamplesChosen");
                            this.$store.commit('addSamplesChosen',{sampleName:"Default", src:/*audioBuffer*/null});
                            this.$store.commit('addSamplesChosen',{sampleName:"Default", src:/*audioBuffer*/null});
                            this.$store.commit('addSamplesChosen',{sampleName:"Default", src:/*audioBuffer*/null});
                            this.$store.commit('addSamplesChosen',{sampleName:"Default", src:/*audioBuffer*/null});
                            this.$store.commit("setBpm", 80);
                            this.$store.commit('updateGainMaster', 1);
                            document.getElementById("volumeMaster").setValue(100);
                            this.$store.commit("updateNbBeats", 4);
                            this.$store.commit("updateNbBeatsRecord", 1);
                            document.getElementById("issueToast").classList.remove("hide");
                            document.getElementById("issueToast").style.transition= "opacity 0.3s";
                            document.getElementById("issueToast").style.opacity = 1;
                            setTimeout(()=>{
                                document.getElementById("issueToast").style.opacity = 0;
                                setTimeout(()=>{document.getElementById("issueToast").classList.add("hide")},300)
                            },4000)
                        },1000)
                    }
                })
                },100)

        },
        readFile(event){
            var readFile = new FileReader();
            readFile.onload = ((event) => {
                var data = JSON.parse(event.target.result)
                this.setSequenceur(data);
            })
            readFile.readAsText(event.target.files[0]);
        },
        activeModal(){
            document.getElementById("saveFileName").click();
        },
        writeFile(){
            var nameFile = document.getElementById("nameFile").value;
            if(nameFile === ""){
                nameFile = "test"
            }
            let sequenceur = { 
                comment: "ATTENTION : NE PAS MODIFIER CE FICHIER SOUS PEINE DE LE RENDRE INUTILISABLE",
                bpm: this.$store.state.bpm,
                masterVolume: document.getElementById('volumeMaster').value/100, 
                nbTemps: this.$store.state.nbBeats,
                nbRecord: this.$store.state.nbBeatsRecord,
                channels: []
            };
            for(var i = 0; i<this.$store.state.samplesChosen.length; i++){
                var sample = this.$store.state.samplesChosen[i];
                var channel = {
                    id: i+1,
                    volume: sample.fxParams.gainValue,
                    pan: sample.fxParams.panValue,
                    name: "Default",
                    src: null,
                    nbSubDiv: sample.timeSubdiv,
                    track: sample.track,
                    filterName: sample.filterName,
                    filterColor: sample.filterColor,
                    filterType: sample.audioNode.filter.type,
                    frequencyInTime: sample.frequencyInTime,
                    frequency: sample.fxParams.frequency,
                    Q: document.getElementById("Q"+sample.id).value,
                }
                sequenceur.channels.push(channel);
            }
            let data = JSON.stringify(sequenceur);
            const blob = new Blob([data], {type: 'text/plain'})
            var a = document.getElementById('fileJsonSave');
            a.download = nameFile + ".json";
            a.href = window.URL.createObjectURL(blob);
            a.click();
            document.getElementById("stopModal").click();
        },
        resetGainMaster(){
            var id = 'volumeMaster';
            document.getElementById(id).value = 100;
            document.getElementById(id).shadowRoot.children[1].children[0].textContent = 100;
            this.$store.commit('updateGainMaster', 1);
        },
        startRecord(){
            this.$store.dispatch("startRecord");
        },
        updateInput(e){
            if(e.target.value < 30){
                e.target.value = 30;
            }
        },
        updateInputNbRecord(e){
            if(e.target.value < 1){
                e.target.value = 1;
            }
        },
        changeButtonAction(){
            if(document.getElementById("modalName").style.display!=="block"){
                if(document.getElementById("btnPlay").classList.contains("d-none")){
                    this.$store.dispatch('stop');  
                    var btnPause = document.getElementById("btnPause");
                    btnPause.classList.add("d-none");
                    btnPause.disabled = true;
                    var btnPlay = document.getElementById("btnPlay");
                    btnPlay.classList.remove("d-none");
                    btnPlay.disabled = false;
                    document.getElementById("progress").style.width = "0%";
                }
                else{
                    this.$store.dispatch('play');
                    var btnPlay = document.getElementById("btnPlay")
                    btnPlay.classList.add("d-none");
                    btnPlay.disabled = true;
                    var btnPause = document.getElementById("btnPause");
                    btnPause.classList.remove("d-none");
                    btnPause.disabled = false;
                }   
            }
        },
        resetMouseDown(){
            this.mouseDown = false;
        },
        upBpm(firstClick=false){
            if(firstClick){
                this.mouseDown = true;
            }
            if(this.mouseDown){
                var value = parseInt(document.getElementById('bpm').value, 10);
                value = isNaN(value) ? 0 : value;
                value++;
                if(value > 300){
                    return;
                }
                document.getElementById('bpm').value = value;
                document.getElementById("inputButtonUp").blur();
                this.$store.commit('setBpm',value);
                window.setTimeout(this.upBpm, 100);
            }
        },
        downBpm(firstClick=false){
            if(firstClick){
                this.mouseDown = true;
            }
            if(this.mouseDown){
                var value = parseInt(document.getElementById('bpm').value, 10);
                value = isNaN(value) ? 0 : value;
                value--;
                if(value < 30){
                    return;
                }
                document.getElementById('bpm').value = value;
                document.getElementById("inputButtonDown").blur();
                this.$store.commit('setBpm',value);
                window.setTimeout(this.downBpm, 100);
            }
        },
        upNbBeats(){
            var value = parseInt(document.getElementById('nbBeats').value, 10);
            value = isNaN(value) ? 0 : value;
            value++;
            if(value > 16){
                return;
            }
            document.getElementById('nbBeats').value = value;
            document.getElementById("inputButtonUpNbBeats").blur();
            this.$store.commit('updateNbBeats',value);
            
        },
        downNbBeats(){
            var value = parseInt(document.getElementById('nbBeats').value, 10);
            value = isNaN(value) ? 0 : value;
            value--;
            if(value < 1){
                return;
            }
            document.getElementById('nbBeats').value = value;
            document.getElementById("inputButtonDownNbBeats").blur();
            this.$store.commit('updateNbBeats',value);
            
        },
        upNbRecord(){
            var value = parseInt(document.getElementById('nbRecord').value, 10);
            value = isNaN(value) ? 0 : value;
            value++;
            if(value > 4){
                return;
            }
            document.getElementById('nbRecord').value = value;
            document.getElementById("inputButtonUpNbRecord").blur();
            this.$store.commit('updateNbBeatsRecord',value);
            
        },
        downNbRecord(){
            var value = parseInt(document.getElementById('nbRecord').value, 10);
            value = isNaN(value) ? 0 : value;
            value--;
            if(value < 1){
                return;
            }
            document.getElementById('nbRecord').value = value;
            document.getElementById("inputButtonDownNbRecord").blur();
            this.$store.commit('updateNbBeatsRecord',value);
            
        },
        fetchFile(url){
        return new Promise((resolve, reject) => {
            fetch(url).then((response) => {
            if (response.ok) {
                resolve(response.blob());
            }
            reject(new Error('Network response was not ok.'));
            });
        }
        )},
        readUploadedFile(file) {
            const temporaryFileReader=new FileReader();

            return new Promise((resolve, reject) => {
                temporaryFileReader.onerror=() => {
                temporaryFileReader.abort();
                reject(new DOMException("Problem parsing input file."));
                };

                temporaryFileReader.onload=() => {
                resolve(temporaryFileReader.result);
                };
                temporaryFileReader.readAsArrayBuffer(file);
            });
        },
        async createAudioBuffer(arrayBuffer){
            var audioCtx = this.getAudioCtx;
            return new Promise((resolve, reject) => {
            audioCtx.decodeAudioData(arrayBuffer, resolve, reject);
            });
        },
        setInDemo(){
            var data = JSON.parse(JSON.stringify(require("@/assets/demo/demo.json")))
            this.setSequenceur(data, true);
            
            setTimeout(async () =>{
                var sourceURL1 = require('@/assets/sounds/kick.wav');
                var blob1 = await this.fetchFile(sourceURL1);
                var arrayBuffer1 = await this.readUploadedFile(blob1);
                var audioBuffer1 = await this.createAudioBuffer(arrayBuffer1);
                this.$store.state.samplesChosen[0].src = audioBuffer1; 
                this.$store.state.samplesChosen[0].name = "kick_Demo";
                document.getElementById("choiceSample"+this.$store.state.samplesChosen[0].id).innerHTML = "kick_De";
               
                
                var sourceURL2 = require('@/assets/sounds/snare.wav');
                var blob2 = await this.fetchFile(sourceURL2);
                var arrayBuffer2 = await this.readUploadedFile(blob2);
                var audioBuffer2 = await this.createAudioBuffer(arrayBuffer2);
                this.$store.state.samplesChosen[1].src = audioBuffer2; 
                this.$store.state.samplesChosen[1].name = "snare_Demo";
                document.getElementById("choiceSample"+this.$store.state.samplesChosen[1].id).innerHTML = "snare_D";
                
                
                
                var sourceURL3 = require('@/assets/sounds/hats.wav');
                var blob3 = await this.fetchFile(sourceURL3);
                var arrayBuffer3 = await this.readUploadedFile(blob3);
                var audioBuffer3 = await this.createAudioBuffer(arrayBuffer3);
                this.$store.state.samplesChosen[2].src = audioBuffer3; 
                this.$store.state.samplesChosen[2].name = "hats_Demo";
                document.getElementById("choiceSample"+this.$store.state.samplesChosen[2].id).innerHTML = "hats_De";
                
                var breakKick = false;
                var breakSnare = false;
                var breakHats = false;
                for(var i=0; i<this.$store.state.samples.length; i++){
                    if(this.$store.state.samples[i].name==="kick_Demo"){
                        breakKick = true
                    }
                    else if(this.$store.state.samples[i].name==="snare_Demo"){
                        breakSnare = true
                    }
                    else if(this.$store.state.samples[i].name==="hats_Demo"){
                        breakHats = true
                    }
                }
                if(!breakKick){
                     this.$store.commit("addSamples", {sampleName:"kick_Demo", buffer: audioBuffer1});
                }
                if(!breakSnare){
                    this.$store.commit("addSamples", {sampleName:"snare_Demo", buffer: audioBuffer2});
                }
                if(!breakHats){
                    this.$store.commit("addSamples", {sampleName:"hats_Demo", buffer: audioBuffer3});
                }

            },800)
        },
        recordFile(){
            var audioElement = document.getElementById("saveRecordFileA");
            var nameOfFile = document.getElementById("nameFileRecord").value;
            if(nameOfFile===''){
                nameOfFile = "test";
            }
            audioElement.download = nameOfFile+".wav";
            audioElement.click();
        }
    },
    mounted() {
        window.addEventListener('keyup', event=>{
            if (event.code === 'Space') {
                event.preventDefault();
                this.changeButtonAction();
            }
        });
        window.addEventListener('keydown', event =>{
            if (event.code === 'Space') {
                event.preventDefault();
            }
        });
        window.addEventListener("resize", this.resizeDiv);
  },
})

</script>

<style scoped>

.master-control{
    padding: 0px 8px 8px 8px;
    border: 2px solid rgb(96, 100, 105);
    background-color: rgba(30, 30 ,30,0.9 );
    border-radius: 0.5rem;
    position: relative;
    -webkit-box-align: center;
    align-items: center;
    box-sizing: border-box;
    transition: border-color 0.2s ease 0s;
    min-width: 1670px;
}
.master-control-label{
    border: 2px solid rgb(96, 100, 105);
}
.control-label{
    border-radius: 1em;
    color: rgb(144, 149, 153);
    background-color: rgb(32, 36, 39);
    font-weight: 600;
    font-size: 0.6rem;
    margin: 0px;
    padding: 0px 4px;
    position: absolute;
    left: 0.5rem;
    top: -0.6em;
    letter-spacing: 0.1em;
    border-radius: 3px;
    line-height: 1em;
    display: block;
}
.buttonAction{
    font-size: 15px;
    width: 60px;
    height: 52px;
}

.buttonActionRecord{
    font-size: 15px;
    width: 50px;
    height: 52px;
    background: rgba(0, 0, 0, 0) linear-gradient(190deg, rgb(25, 25, 29) 0%, rgb(48, 48, 54) 50%, rgb(10, 14, 10) 51%, rgb(41, 41, 45) 100%) repeat scroll 0% 0%;
}

.buttonActionLoad{
    font-size: 15px;
    width: 50px;
    height: 52px;
}

.divInputBpm {
    border: 2px solid rgb(96, 100, 105);
    border-radius: 0.5rem;
    display: flex;
    position: relative;
    box-sizing: border-box;
    background: rgba(0, 0, 0, 0) linear-gradient(190deg, rgb(25, 25, 29) 0%, rgb(48, 48, 54) 50%, rgb(10, 14, 10) 51%, rgb(41, 41, 45) 100%) repeat scroll 0% 0%;
    transition: border-color 0.2s ease 0s;
    width: 92px;
    height: 52px;
}

.labelInputBpm {
    color: rgb(144, 149, 153);
    background-color: rgb(32, 36, 39);
    font-weight: 600;
    font-size: 0.6rem;
    margin: 0px;
    padding: 0px 4px;
    position: absolute;
    left: 0.5rem;
    top: -0.6em;
    letter-spacing: 0.1em;
    display: block;
    line-height: 1em;
}

input[type=number]::-webkit-inner-spin-button, 
input[type=number]::-webkit-outer-spin-button {
    -webkit-appearance: none;
}

.bpm-text-input {
    -webkit-appearance: none;
    appearance: textfield;
}

.inputBpm {
    color: rgb(244, 83, 58);
    background-color: transparent;
    font-weight: 500;
    font-size: 1.5rem;
    margin: 0px;
    padding: 0.3rem 0px 0px 0.7rem;
    position: relative;
    z-index: 1;
    width: 3.5rem;
    display: block;
    border: medium none;
    outline: none;
}

.divInputButtons {
    flex-direction: column;
    display: flex;
    box-sizing: border-box;
}

.inputButton {
    color: white;
    background-color: transparent;
    padding: 0px;
    border: medium none;
    font-weight: bold;
    width: 2rem;
    flex: 1 1 auto;
    touch-action: manipulation;
}
#inputButtonUp, #inputButtonUpNbRecord{
    border-radius: 0px 0.5rem 0px 0px;
}

#inputButtonDown, #inputButtonDownNbRecord{
    border-radius: 0px 0px 0.5rem;
}

.divInputButtons button:active{
    background-color: black ;
}

.selector-container{
    margin-top: -4rem;
    box-sizing: border-box;
    width: 5rem;
    height: 3rem;
    align-items: center;
    justify-content: center;
    color: ghostwhite;
}
.custom-select{
    line-height: 2rem;
    height: 2rem;
}
.knob-slot{
    box-sizing: border-box;
}
.knob-name{
    padding: 0;
    margin: 0 0 4px;
    font-weight: bold;
    text-align: center;
    font-size: 0.7rem;
    line-height: 1em;
    color: ghostwhite;
    display: block;
    text-transform: uppercase;
    width: 3rem;
}
.knob{
    display: flex;
    align-items: baseline;
    -webkit-box-align: baseline;
    box-sizing: border-box;
}
.knob-label{
    margin: 0;
    padding: 0;
    opacity: 0.7;
    line-height: 1em;
    display: block;
    font-size: 0.7em;
    text-transform: uppercase;
    color: ghostwhite;
}
.btn-demo{
    box-shadow: none !important;
    height: 52px;
}
.mybtn-info{
    box-shadow: none !important;
    height: 52px;
    width: 52px;
}
.modal-content{
    background-color: #222;
    color: ghostwhite;
}
.control-slot{
    box-sizing: border-box;
    margin: 0.4rem 0.25rem;
    padding: 0.5rem 1.5rem 1.5rem 1.5rem;
    background-color: rgb(136, 136, 136);
    border-radius: 6px;
}
.divMasterScope{
    margin: auto 50px auto 50px; 
    padding-bottom:0.5rem
}
.btn-style{
    background: rgba(217, 83, 79, 0) linear-gradient(190deg, rgb(25, 25, 29) 0%, rgb(48, 48, 54) 50%, rgb(10, 14, 10) 51%, rgb(41, 41, 45) 100%) repeat scroll 0% 0%;
    border-width: 2px;
}
.modal-dialog-info{
    max-width: 900px !important;
}
</style>
